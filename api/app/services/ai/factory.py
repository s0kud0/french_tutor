from core.config import settings
from services.ai.openai_provider import OpenAIProvider


def get_ai_provider():

    if settings.AI_PROVIDER == "openai":
        return OpenAIProvider()

    raise ValueError(
        f"Unknown AI provider: {settings.AI_PROVIDER}"
    )
