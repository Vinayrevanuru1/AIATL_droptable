# db_utils.py
import psycopg2

# Database connection
conn = psycopg2.connect(
    database="postgres",
    user="Yaniv",
    password="test",
    host="35.224.255.227",
    port="5432"
)

def get_patient_context(patient_id):
    """Retrieve patient data and set up initial memory context for chat."""
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users WHERE user_id = %s;''', (patient_id,))
    patient_data = cursor.fetchone()
    cursor.close()

    # Format patient data into memory context if available
    if patient_data:
        patient_context = {
            "description": "Patient information",
            "expected_output": f"Context for patient ID {patient_id}",
            "content": {
                "ID": patient_data[0],
                "password": patient_data[1],
                "name": patient_data[2],
                "email_address": patient_data[3],
                "address": patient_data[4],
                "phone_number": patient_data[5],
                "medical_history": patient_data[6],
                "upcoming_appointment": patient_data[7],
                "department": patient_data[8],
                "last_appointment_date": patient_data[9],
                "current_medication": patient_data[10],
            }
        }
        greeting_message = f"Hello, {patient_data[2]}! I'm here to help with your medical needs today."
        return [patient_context], greeting_message
    else:
        return [], "Patient not found."
