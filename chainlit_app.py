import chainlit as cl
from db_utils import get_patient_context
from intent_bot import IntentBot
from crewai import Task, Crew
from agents import supervisor

# Initialize Intent Bot globally
intent_bot = IntentBot()

async def process_question(patient_id, user_question, memory):
    """Processes the user question through the intent bot and returns the response."""

    # Use Intent Bot to identify the intent and select the appropriate agent
    agent, intent = intent_bot.identify_intent(user_question)

    # Retrieve patient's name from memory for a personalized response
    patient_name = memory[0]["content"].get("name", "there") if memory else "there"

    # Create the task for the identified agent with patient memory context
    task = Task(
        description=f"Provide response for {intent} considering patient name ({patient_name}) and previous chat history.",
        agent=agent,
        expected_output=f"{intent.capitalize()} response with patient-specific details.",
        context=memory  # Pass patient-specific memory as context
    )

    # Run the task through Crew to obtain the agent's response
    crew_result = Crew(
        name=f"{intent.capitalize()} Response Team",
        agents=[agent],
        tasks=[task],
        verbose=True
    ).kickoff()

    # Store the main agent's response in memory
    memory.append({
        "description": f"{intent.capitalize()} response",
        "expected_output": str(crew_result),
        "role": intent.capitalize(),
        "content": str(crew_result)
    })

    response = f"{intent.capitalize()} Specialist: {str(crew_result)}"

    # If a non-supervisor agent handled the task, follow up with the supervisor
    if agent != supervisor:
        supervisor_task = Task(
            description=f"Enhance {intent} response with awareness of patient details like name ({patient_name}).",
            agent=supervisor,
            expected_output="Friendly summary and additional guidance with patient-specific details.",
            context=memory
        )

        # Run the supervisor task to enhance the response
        supervisor_result = Crew(
            name="Supervisor Enhancement",
            agents=[supervisor],
            tasks=[supervisor_task],
            verbose=True
        ).kickoff()

        # Store the supervisor's response in memory
        memory.append({
            "description": "Supervisor response",
            "expected_output": str(supervisor_result),
            "role": "Supervisor",
            "content": str(supervisor_result)
        })

        response += f"\nSupervisor: {str(supervisor_result)}"

    return response


@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat with the patient's context."""
    patient_id = "1"  # Sample patient ID; this could be dynamic if needed
    memory, greeting_message = get_patient_context(patient_id)

    if memory:
        # Display initial greeting message
        await cl.Message(content=greeting_message).send()
        # Save the patient memory context for the session
        cl.user_session.set("memory", memory)
        cl.user_session.set("patient_id", patient_id)
    else:
        await cl.Message(content="Patient not found.").send()


@cl.on_message
async def on_message(message):
    """Process each user message."""
    # Extract the text content from the Message object
    user_question = message.content

    # Retrieve memory context and patient ID from session
    memory = cl.user_session.get("memory")
    patient_id = cl.user_session.get("patient_id")

    if not memory or not patient_id:
        await cl.Message(content="Session not initialized. Please restart the chat.").send()
        return

    # Add user question to memory
    memory.append({
        "description": "User input",
        "expected_output": user_question,
        "role": "user",
        "content": user_question
    })

    # Process the question and get the response
    response = await process_question(patient_id, user_question, memory)

    # Update memory in the session
    cl.user_session.set("memory", memory)

    # Display the response to the user
    await cl.Message(content=response).send()

