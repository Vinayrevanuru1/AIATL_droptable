


# import chainlit as cl
# import pandas as pd
# from db_utils import get_patient_context
# from intent_bot import IntentBot
# from crewai import Task, Crew
# from agents import supervisor

# # Initialize Intent Bot globally
# intent_bot = IntentBot()

# # Function to load past interactions from a TSV file
# def load_past_interactions(file_path="chat_history.tsv"):
#     """Load past interactions from a TSV file."""
#     try:
#         df = pd.read_csv(file_path, sep='\t')
#         return df.to_dict(orient="records")
#     except FileNotFoundError:
#         print("TSV file not found.")
#         return []

# async def display_past_interactions(memory):
#     """Display past interactions to the user at chat start and add them to memory."""
#     interactions = load_past_interactions()
#     for interaction in interactions:
#         question = interaction.get("question", "Question missing")
#         response = interaction.get("response", "Response missing")

#         # Display each question-response pair
#         await cl.Message(content=f"**User**: {question}").send()
#         await cl.Message(content=f"**Assistant**: {response}").send()

#         # Add each interaction to memory for future reference
#         memory.append({
#             "description": "Past interaction",
#             "role": "user",
#             "content": question,
#             "expected_output": "User question"  # Ensuring `expected_output` is set
#         })
#         memory.append({
#             "description": "Past interaction",
#             "role": "assistant",
#             "content": response,
#             "expected_output": "Assistant response"  # Ensuring `expected_output` is set
#         })

# async def process_question(patient_id, user_question, memory):
#     """Processes the user question through the intent bot and returns the response."""

#     # Use Intent Bot to identify the intent and select the appropriate agent
#     agent, intent = intent_bot.identify_intent(user_question)

#     # Retrieve patient's name from memory for a personalized response
#     patient_name = memory[0]["content"].get("name", "there") if memory else "there"

#     # Create the task for the identified agent with patient memory context
#     task = Task(
#         description=f"Provide response for {intent} considering patient name ({patient_name}) and previous chat history.",
#         agent=agent,
#         expected_output=f"{intent.capitalize()} response with patient-specific details.",
#         context=memory  # Pass patient-specific memory as context
#     )

#     # Run the task through Crew to obtain the agent's response
#     crew_result = Crew(
#         name=f"{intent.capitalize()} Response Team",
#         agents=[agent],
#         tasks=[task],
#         verbose=True
#     ).kickoff()

#     # Store the main agent's response in memory
#     memory.append({
#         "description": f"{intent.capitalize()} response",
#         "expected_output": str(crew_result),
#         "role": intent.capitalize(),
#         "content": str(crew_result)
#     })

#     response = f"{intent.capitalize()} Specialist: {str(crew_result)}"

#     # If a non-supervisor agent handled the task, follow up with the supervisor
#     if agent != supervisor:
#         supervisor_task = Task(
#             description=f"Enhance {intent} response with awareness of patient details like name ({patient_name}).",
#             agent=supervisor,
#             expected_output="Friendly summary and additional guidance with patient-specific details.",
#             context=memory
#         )

#         # Run the supervisor task to enhance the response
#         supervisor_result = Crew(
#             name="Supervisor Enhancement",
#             agents=[supervisor],
#             tasks=[supervisor_task],
#             verbose=True
#         ).kickoff()

#         # Store the supervisor's response in memory
#         memory.append({
#             "description": "Supervisor response",
#             "expected_output": str(supervisor_result),
#             "role": "Supervisor",
#             "content": str(supervisor_result)
#         })

#         response += f"\nSupervisor: {str(supervisor_result)}"

#     return response

# @cl.on_chat_start
# async def on_chat_start():
#     """Initialize the chat with the patient's context and display past interactions."""
#     patient_id = "1"  # Sample patient ID; this could be dynamic if needed
#     memory, greeting_message = get_patient_context(patient_id)

#     if memory:
#         # Display initial greeting message
#         await cl.Message(content=greeting_message).send()
        
#         # Load and display past interactions
#         await display_past_interactions(memory)
        
#         # Save the patient memory context for the session
#         cl.user_session.set("memory", memory)
#         cl.user_session.set("patient_id", patient_id)
#     else:
#         await cl.Message(content="Patient not found.").send()

# @cl.on_message
# async def on_message(message):
#     """Process each user message."""
#     # Extract the text content from the Message object
#     user_question = message.content

#     # Retrieve memory context and patient ID from session
#     memory = cl.user_session.get("memory")
#     patient_id = cl.user_session.get("patient_id")

#     if not memory or not patient_id:
#         await cl.Message(content="Session not initialized. Please restart the chat.").send()
#         return

#     # Add user question to memory
#     memory.append({
#         "description": "User input",
#         "expected_output": user_question,
#         "role": "user",
#         "content": user_question
#     })

#     # Process the question and get the response
#     response = await process_question(patient_id, user_question, memory)

#     # Update memory in the session
#     cl.user_session.set("memory", memory)

#     # Display the response to the user
#     await cl.Message(content=response).send()




#############################################################################################################################


# import chainlit as cl
# import pandas as pd
# from db_utils import get_patient_context
# from intent_bot import IntentBot
# from crewai import Task, Crew
# from agents import supervisor

# # Load user credentials from TSV file
# credentials_df = pd.read_csv("passwords.tsv", sep='\t')

# # Initialize Intent Bot globally
# intent_bot = IntentBot()

# # Function to verify user credentials
# def verify_login(user_id, password):
#     """Verify user credentials."""
#     user = credentials_df[(credentials_df["user_id"] == user_id) & (credentials_df["password"] == password)]
#     return not user.empty  # Returns True if credentials match

# # Function to load past interactions from TSV
# def load_past_interactions(file_path="chat_history.tsv"):
#     """Load past interactions from a TSV file."""
#     try:
#         df = pd.read_csv(file_path, sep='\t')
#         return df.to_dict(orient="records")
#     except FileNotFoundError:
#         print("TSV file not found.")
#         return []

# async def display_past_interactions(memory):
#     """Display past interactions to the user at chat start and add them to memory."""
#     interactions = load_past_interactions()
#     for interaction in interactions:
#         question = interaction.get("question", "Question missing")
#         response = interaction.get("response", "Response missing")

#         await cl.Message(content=f"**User**: {question}").send()
#         await cl.Message(content=f"**Assistant**: {response}").send()

#         memory.append({
#             "description": "Past interaction",
#             "role": "user",
#             "content": question
#         })
#         memory.append({
#             "description": "Past interaction",
#             "role": "assistant",
#             "content": response
#         })

# async def process_question(patient_id, user_question, memory):
#     """Processes the user question through the intent bot and returns the response."""
#     agent, intent = intent_bot.identify_intent(user_question)
#     patient_name = memory[0]["content"].get("name", "there") if memory else "there"
    
#     task = Task(
#         description=f"Provide response for {intent} considering patient name ({patient_name}) and previous chat history.",
#         agent=agent,
#         expected_output=f"{intent.capitalize()} response with patient-specific details.",
#         context=memory
#     )
    
#     crew_result = Crew(
#         name=f"{intent.capitalize()} Response Team",
#         agents=[agent],
#         tasks=[task],
#         verbose=True
#     ).kickoff()

#     memory.append({
#         "description": f"{intent.capitalize()} response",
#         "expected_output": str(crew_result),
#         "role": intent.capitalize(),
#         "content": str(crew_result)
#     })

#     response = f"{intent.capitalize()} Specialist: {str(crew_result)}"
    
#     if agent != supervisor:
#         supervisor_task = Task(
#             description=f"Enhance {intent} response with awareness of patient details like name ({patient_name}).",
#             agent=supervisor,
#             expected_output="Friendly summary and additional guidance with patient-specific details.",
#             context=memory
#         )
        
#         supervisor_result = Crew(
#             name="Supervisor Enhancement",
#             agents=[supervisor],
#             tasks=[supervisor_task],
#             verbose=True
#         ).kickoff()

#         memory.append({
#             "description": "Supervisor response",
#             "expected_output": str(supervisor_result),
#             "role": "Supervisor",
#             "content": str(supervisor_result)
#         })

#         response += f"\nSupervisor: {str(supervisor_result)}"

#     return response


# @cl.on_chat_start
# async def on_chat_start():
#     """Initialize the login process."""
#     # Set session state to start login
#     cl.user_session.set("login_state", "awaiting_user_id")
#     await cl.Message(content="Welcome! Please enter your User ID to start.").send()


# @cl.on_message
# async def on_message(message):
#     """Process each user message based on the current login state or authenticated chat."""
#     login_state = cl.user_session.get("login_state")
#     memory = cl.user_session.get("memory")

#     # Handle login process
#     if login_state == "awaiting_user_id":
#         # Store user_id and prompt for password
#         cl.user_session.set("user_id", message.content.strip())
#         cl.user_session.set("login_state", "awaiting_password")
#         await cl.Message(content="Please enter your Password.").send()

#     elif login_state == "awaiting_password":
#         # Get the stored user_id and entered password
#         user_id = cl.user_session.get("user_id")
#         password = message.content.strip()

#         # Verify credentials
#         if verify_login(user_id, password):
#             # Successful login
#             cl.user_session.set("authenticated", True)
#             cl.user_session.set("login_state", None)  # Clear login state

#             # Initialize patient context and memory
#             patient_id = user_id
#             memory, greeting_message = get_patient_context(patient_id)
#             cl.user_session.set("memory", memory)
#             cl.user_session.set("patient_id", patient_id)

#             # Display greeting and past interactions
#             await cl.Message(content=greeting_message).send()
#             await display_past_interactions(memory)
#         else:
#             # Failed login attempt
#             await cl.Message(content="Invalid credentials. Please restart the chat and try again.").send()
#             cl.user_session.clear()  # Clear session on failed login

#     elif cl.user_session.get("authenticated"):
#         # Process user questions if authenticated
#         user_question = message.content
#         memory = cl.user_session.get("memory")
#         patient_id = cl.user_session.get("patient_id")

#         # Process the question and get the response
#         response = await process_question(patient_id, user_question, memory)

#         # Update memory and session
#         memory.append({
#             "description": "User input",
#             "expected_output": user_question,
#             "role": "user",
#             "content": user_question
#         })
#         cl.user_session.set("memory", memory)

#         # Display the response to the user
#         await cl.Message(content=response).send()
#     else:
#         await cl.Message(content="Please log in to access the chat. Restart the chat to try again.").send()



########################################################


import chainlit as cl
from db_utils import get_patient_context, verify_login  # Import from db_utils
from intent_bot import IntentBot
from crewai import Task, Crew
from agents import supervisor

# Initialize Intent Bot globally
intent_bot = IntentBot()

async def display_past_interactions(memory):
    """Display past interactions to the user at chat start and add them to memory."""
    interactions = load_past_interactions()  # Assuming load_past_interactions function exists
    for interaction in interactions:
        question = interaction.get("question", "Question missing")
        response = interaction.get("response", "Response missing")

        await cl.Message(content=f"**User**: {question}").send()
        await cl.Message(content=f"**Assistant**: {response}").send()

        memory.append({
            "description": "Past interaction",
            "role": "user",
            "content": question
        })
        memory.append({
            "description": "Past interaction",
            "role": "assistant",
            "content": response
        })

async def process_question(patient_id, user_question, memory):
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

    return response

@cl.on_chat_start
async def on_chat_start():
    """Initialize the login process."""
    # Set session state to start login
    cl.user_session.set("login_state", "awaiting_user_id")
    await cl.Message(content="Welcome! Please enter your User ID to start.").send()

@cl.on_message
async def on_message(message):
    """Process each user message based on the current login state or authenticated chat."""
    login_state = cl.user_session.get("login_state")

    # Handle login process
    if login_state == "awaiting_user_id":
        # Store user_id and prompt for password
        cl.user_session.set("user_id", message.content.strip())
        cl.user_session.set("login_state", "awaiting_password")
        await cl.Message(content="Please enter your Password.").send()

    elif login_state == "awaiting_password":
        # Get the stored user_id and entered password
        user_id = cl.user_session.get("user_id")
        password = message.content.strip()

        # Verify credentials
        if verify_login(user_id, password):
            # Successful login
            cl.user_session.set("authenticated", True)
            cl.user_session.set("login_state", None)  # Clear login state

            # Initialize patient context and memory
            patient_id = user_id
            memory, greeting_message = get_patient_context(patient_id)
            cl.user_session.set("memory", memory)
            cl.user_session.set("patient_id", patient_id)

            # Display greeting and past interactions
            await cl.Message(content=greeting_message).send()
            await display_past_interactions(memory)
        else:
            # Failed login attempt
            await cl.Message(content="Invalid credentials. Please restart the chat and try again.").send()
            cl.user_session.clear()  # Clear session on failed login

    elif cl.user_session.get("authenticated"):
        # Process user questions if authenticated
        user_question = message.content
        memory = cl.user_session.get("memory")
        patient_id = cl.user_session.get("patient_id")

        # Process the question and get the response
        response = await process_question(patient_id, user_question, memory)

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
