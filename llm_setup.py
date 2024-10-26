# llm_setup.py
import os
from crewai import LLM
from langchain.llms.base import BaseLLM
from pydantic import BaseModel, Field
from typing import Optional, List, Dict

# Set up Google Application credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "noble-kingdom-439722-u5-8ddb44363387.json"

# Initialize CrewAI's LLM for Vertex AI
crewai_llm = LLM(
    model="vertex_ai/gemini-1.5-flash",
    temperature=0.8,
    max_tokens=1500,
    stop=["END"],
    vertex_credentials=os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
)

# Define a LangChain-compatible wrapper for CrewAI LLM
class CrewAILLM(BaseLLM, BaseModel):
    llm: LLM = Field(default=crewai_llm)

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _generate(self, prompt: str, stop: Optional[List[str]] = None) -> Dict:
        response = self.llm.generate(prompt)
        return {"text": response}

    @property
    def identifying_params(self):
        return {"model": "vertex_ai/gemini-1.5-pro"}

wrapped_llm = CrewAILLM()
