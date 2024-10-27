

# db_utils.py
# import psycopg2
# import bcrypt

# # Database connection
# conn = psycopg2.connect(
#     database="postgres",
#     user="Yaniv",
#     password="test",
#     host="35.224.255.227",
#     port="5432"
# )

# def get_patient_context(patient_id):
#     """Retrieve patient data and set up initial memory context for chat."""
#     cursor = conn.cursor()
#     cursor.execute('''SELECT * FROM users WHERE user_id = %s;''', (patient_id,))
#     patient_data = cursor.fetchone()
#     cursor.close()

#     # Format patient data into memory context if available
#     if patient_data:
#         patient_context = {
#             "description": "Patient information",
#             "expected_output": f"Context for patient ID {patient_id}",
#             "content": {
#                 "ID": patient_data[0],
#                 "password": patient_data[1],  # Hashed password
#                 "name": patient_data[2],
#                 "email_address": patient_data[3],
#                 "address": patient_data[4],
#                 "phone_number": patient_data[5],
#                 "medical_history": patient_data[6],
#                 "upcoming_appointment": patient_data[7],
#                 "department": patient_data[8],
#                 "last_appointment_date": patient_data[9],
#                 "current_medication": patient_data[10],
#             }
#         }
#         greeting_message = f"Hello, {patient_data[2]}! I'm here to help with your medical needs today."
#         return [patient_context], greeting_message
#     else:
#         return [], "Patient not found."

# def hash_password(password):
#     """Hash a plaintext password."""
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#     return hashed_password

# def verify_login(user_id, password):
#     """Verify login by checking if the user_id and hashed password match."""
#     cursor = conn.cursor()
#     cursor.execute('''SELECT password FROM users WHERE user_id = %s;''', (user_id,))
#     result = cursor.fetchone()
#     cursor.close()

#     if result:
#         stored_hashed_password = result[0]
#         # Compare stored hashed password with the entered password
#         return bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8'))
#     return False



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

def verify_login(user_id, password):
    """Verify user credentials by comparing hashed password from the database."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT password FROM users WHERE user_id = %s;", (user_id,))
        user_data = cursor.fetchone()

    if user_data:
        stored_password = user_data[0]
        # Compare the hashed password stored in the database with the provided password
        return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))
    return False

def get_patient_context(patient_id):
    """Retrieve patient data and set up initial memory context for chat."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s;", (patient_id,))
    patient_data = cursor.fetchone()
    cursor.close()

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

def get_conversations(user_id):
    """Retrieve past conversations for a given user_id."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT question, response, timestamp FROM conversations WHERE user_id = %s ORDER BY timestamp;", (user_id,))
        conversations = cursor.fetchall()
    return conversations

