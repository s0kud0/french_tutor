import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://tutor:tutorpass@postgres:5432/tutor",
    )


settings = Settings()
