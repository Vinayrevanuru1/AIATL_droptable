import chainlit as cl
from db_utils import get_patient_context, verify_login, get_conversations, save_conversation  # Import save_conversation
from intent_bot import IntentBot
from crewai import Task, Crew
from agents import supervisor

# Initialize Intent Bot globally
intent_bot = IntentBot()

async def display_past_interactions(email, memory):
    """Display past interactions to the user at chat start and add them to memory."""
    interactions = get_conversations(email)  # Fetch interactions from the database

    if not interactions:
        await cl.Message(content="No past interactions found.").send()
        return

    for interaction in interactions:
        question = interaction.get("question", "Question missing")
        response = interaction.get("response", "Response missing")

        await cl.Message(content=f"**User**: {question}").send()
        await cl.Message(content=f"**Assistant**: {response}").send()

        memory.append({
            "description": "Past interaction",
            "role": "user",
            "content": question,
            "expected_output": "User question"
        })
        memory.append({
            "description": "Past interaction",
            "role": "assistant",
            "content": response,
            "expected_output": "Assistant response"
        })

async def process_question(email, user_question, memory):
    """Processes the user question through the intent bot and returns the response."""
    agent, intent = intent_bot.identify_intent(user_question)
    patient_name = memory[0]["content"].get("name", "there") if memory else "there"
    
    task = Task(
        description=f"Provide response for {intent} considering patient name ({patient_name}) and previous chat history.",
        agent=agent,
        expected_output=f"{intent.capitalize()} response with patient-specific details.",
        context=memory
    )
    
    crew_result = Crew(
        name=f"{intent.capitalize()} Response Team",
        agents=[agent],
        tasks=[task],
        verbose=True
    ).kickoff()

    memory.append({
        "description": f"{intent.capitalize()} response",
        "expected_output": str(crew_result),
        "role": intent.capitalize(),
        "content": str(crew_result)
    })

    response = f"{intent.capitalize()} Specialist: {str(crew_result)}"
    
    if agent != supervisor:
        supervisor_task = Task(
            description=f"Enhance {intent} response with awareness of patient details like name ({patient_name}).",
            agent=supervisor,
            expected_output="Friendly summary and additional guidance with patient-specific details.",
            context=memory
        )
        
        supervisor_result = Crew(
            name="Supervisor Enhancement",
            agents=[supervisor],
            tasks=[supervisor_task],
            verbose=True
        ).kickoff()

        memory.append({
            "description": "Supervisor response",
            "expected_output": str(supervisor_result),
            "role": "Supervisor",
            "content": str(supervisor_result)
        })

        response += f"\nSupervisor: {str(supervisor_result)}"

    # Save the question and response in the database
    user_id = memory[0]["content"]["ID"]  # Get user_id from memory context
    save_conversation(user_id, user_question, response)

    return response

@cl.on_chat_start
async def on_chat_start():
    """Initialize the login process."""
    # Set session state to start login
    cl.user_session.set("login_state", "awaiting_email")
    await cl.Message(content="Welcome! Please enter your Email to start.").send()

@cl.on_message
async def on_message(message):
    """Process each user message based on the current login state or authenticated chat."""
    login_state = cl.user_session.get("login_state")

    # Handle login process
    if login_state == "awaiting_email":
        # Store email and prompt for password
        cl.user_session.set("email", message.content.strip())
        cl.user_session.set("login_state", "awaiting_password")
        await cl.Message(content="Please enter your Password.").send()

    elif login_state == "awaiting_password":
        # Get the stored email and entered password
        email = cl.user_session.get("email")
        password = message.content.strip()

        # Verify credentials
        if verify_login(email, password):
            # Successful login
            cl.user_session.set("authenticated", True)
            cl.user_session.set("login_state", None)  # Clear login state

            # Initialize patient context and memory
            memory, greeting_message = get_patient_context(email)
            cl.user_session.set("memory", memory)
            cl.user_session.set("email", email)

            # Display greeting and past interactions
            await cl.Message(content=greeting_message).send()
            await display_past_interactions(email, memory)  # Pass email to fetch past interactions
        else:
            # Failed login attempt
            await cl.Message(content="Invalid credentials. Please restart the chat and try again.").send()
            # Manually clear session variables instead of using clear()
            cl.user_session.set("authenticated", None)
            cl.user_session.set("email", None)
            cl.user_session.set("login_state", None)

    elif cl.user_session.get("authenticated"):
        # Process user questions if authenticated
        user_question = message.content
        memory = cl.user_session.get("memory")
        email = cl.user_session.get("email")

        # Process the question and get the response
        response = await process_question(email, user_question, memory)

        # Update memory and session
        memory.append({
            "description": "User input",
            "expected_output": user_question,
            "role": "user",
            "content": user_question
        })
        cl.user_session.set("memory", memory)

        # Display the response to the user
        await cl.Message(content=response).send()
    else:
        await cl.Message(content="Please log in to access the chat. Restart the chat to try again.").send()
