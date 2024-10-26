# medical_assistant_chat.py
from db_utils import get_patient_context
from intent_bot import IntentBot
from crewai import Task, Crew
from agents import supervisor

def medical_assistant_chat_with_intent_bot(patient_id):
    intent_bot = IntentBot()
    memory, greeting_message = get_patient_context(patient_id)

    # Retrieve patient's name from memory for a personalized greeting
    patient_name = memory[0]["content"].get("name", "there") if memory else "there"
    print(f"{greeting_message} Type 'exit' to end the chat.")

    while True:
        user_question = input("You: ")
        if user_question.lower() == "exit":
            print("Thank you for chatting with us! Take care!")
            break

        # Add user input to memory
        memory.append({
            "description": "User input",
            "expected_output": user_question,
            "role": "user",
            "content": user_question
        })

        # Use Intent Bot to identify the intent and assign the appropriate agent
        agent, intent = intent_bot.identify_intent(user_question)

        # Create the task with patient memory context
        task = Task(
            description=f"Provide response for {intent} considering patient name ({patient_name}) and previous chat history.",
            agent=agent,
            expected_output=f"{intent.capitalize()} response with patient-specific details.",
            context=memory  # Pass memory with patient context
        )

        # Run the task to obtain the agent's response
        crew_result = Crew(
            name=f"{intent.capitalize()} Response Team",
            agents=[agent],
            tasks=[task],
            verbose=True
        ).kickoff()

        # Display and store the agent's response in memory
        print(f"{intent.capitalize()} Specialist:", str(crew_result))
        memory.append({
            "description": f"{intent.capitalize()} response",
            "expected_output": str(crew_result),
            "role": intent.capitalize(),
            "content": str(crew_result)
        })

        # If the response comes from a non-supervisor agent, add a supervisor follow-up
        if agent != supervisor:
            supervisor_task = Task(
                description=f"Enhance {intent} response with awareness of patient details like name ({patient_name}).",
                agent=supervisor,
                expected_output="Friendly summary and additional guidance with patient-specific details.",
                context=memory
            )

            # Run the supervisor enhancement
            supervisor_result = Crew(
                name="Supervisor Enhancement",
                agents=[supervisor],
                tasks=[supervisor_task],
                verbose=True
            ).kickoff()

            # Display and store the supervisor's response in memory
            print("Supervisor:", str(supervisor_result))
            memory.append({
                "description": "Supervisor response",
                "expected_output": str(supervisor_result),
                "role": "Supervisor",
                "content": str(supervisor_result)
            })

# Run the chat with a sample patient ID
if __name__ == "__main__":
    medical_assistant_chat_with_intent_bot(patient_id="1")
