import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt

# Database connection setup
conn = psycopg2.connect(
    database="postgres",
    user="Yaniv",
    password="test",
    host="35.224.255.227",
    port="5432"
)

def verify_login(email, password):
    """Verify user credentials by comparing hashed password from the database using email."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT password FROM users WHERE email_address = %s;", (email,))
        user_data = cursor.fetchone()

    if user_data:
        stored_password = user_data[0]
        # Compare the hashed password stored in the database with the provided password
        return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))
    return False

def get_patient_context(email):
    """Retrieve patient data and set up initial memory context for chat using email."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email_address = %s;", (email,))
    patient_data = cursor.fetchone()
    cursor.close()

    if patient_data:
        patient_context = {
            "description": "Patient information",
            "expected_output": f"Context for patient email {email}",
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

def get_conversations(email):
    """Retrieve past conversations for a given email."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT question, response, timestamp FROM conversations WHERE user_id = (SELECT user_id FROM users WHERE email_address = %s) ORDER BY timestamp;", (email,))
        conversations = cursor.fetchall()
    return conversations
