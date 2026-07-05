from services.ai.factory import get_ai_provider

provider = get_ai_provider()

print(provider.generate_reply([]))
