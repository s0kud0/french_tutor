import time
from sqlmodel import SQLModel, create_engine, Session

from core.config import settings

DATABASE_URL = settings.DATABASE_URL

# IMPORTANT: add retry-friendly settings
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  # checks connection before using it
)


def get_session():
    with Session(engine) as session:
        yield session
