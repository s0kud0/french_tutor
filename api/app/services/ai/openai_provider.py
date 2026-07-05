from openai import OpenAI
from services.ai.base import AIProvider


class OpenAIProvider(AIProvider):
    def __init__(self):
        self.client = OpenAI()

    def chat(self, prompt: str) -> str:
        response = self.client.responses.create(
            model="gpt-5-mini",
            input=prompt,
        )
        return response.output_text
