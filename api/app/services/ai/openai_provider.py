from openai import OpenAI
from core.config import settings
from services.ai.base import AIProvider


class OpenAIProvider(AIProvider):
    def __init__(self):
        self.client = OpenAI()

    def chat(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=settings.OPENAI_MODEL,
            input=prompt,
        )
        return response.output_text
