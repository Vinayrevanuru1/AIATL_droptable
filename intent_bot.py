from agents import (
    appointment_scheduler,
    cancer_specialist,
    dermatologist,
    physician,
    xray_analyzer,
    mental_health_assistant,
    supervisor,
)


class IntentBot:
    def __init__(self):
        # Intent keywords and associated agent
        self.intent_map = {
            "scheduling appointment": {
                "keywords": ["schedule", "book", "appointment", "availability", "cancel appointment", "reschedule"],
                "agent": appointment_scheduler
            },
            "cancer-related inquiry": {
                "keywords": ["cancer", "oncology", "tumor", "chemotherapy", "radiation", "symptoms"],
                "agent": cancer_specialist
            },
            "skin and dermatology": {
                "keywords": ["rash", "skin", "acne", "eczema", "dermatologist", "itching"],
                "agent": dermatologist
            },
            "general medical inquiry": {
                "keywords": ["general health", "fever", "cough", "sore throat", "physician", "check-up"],
                "agent": physician
            },
            "image/x-ray analysis": {
                "keywords": ["X-ray", "CT scan", "MRI", "image analysis", "scan"],
                "agent": xray_analyzer
            },
            "mental health support": {
                "keywords": ["anxiety", "stress", "depression", "mental health", "therapy", "counseling"],
                "agent": mental_health_assistant
            }
        }

    def identify_intent(self, question: str):
        question_lower = question.lower()
        for intent, details in self.intent_map.items():
            if any(keyword in question_lower for keyword in details["keywords"]):
                return details["agent"], intent
        return supervisor, "general guidance"