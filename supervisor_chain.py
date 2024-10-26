# supervisor_chain.py
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from llm_setup import wrapped_llm

class MedicalSupervisorChain(LLMChain):
    def __init__(self):
        messages = [
            ("system", "You’re the supervisor of a friendly and knowledgeable medical assistant team. Greet users warmly and help direct questions to the right specialist."),
            ("user", "{question}")
        ]
        prompt = ChatPromptTemplate(input_variables=["question"], messages=messages)
        super().__init__(prompt=prompt, llm=wrapped_llm)
