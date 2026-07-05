import time
from sqlmodel import SQLModel
from sqlalchemy.exc import OperationalError

from core.database import engine
from models.chat import Session, Message


def init_db(retries: int = 10, delay: float = 2.0):
    print("🚀 Initializing database...")

    for i in range(retries):
        try:
            SQLModel.metadata.create_all(engine)
            print("✅ Database tables created successfully")
            return
        except OperationalError as e:
            print(f"⏳ DB not ready yet (attempt {i+1}/{retries})...")
            time.sleep(delay)

    raise Exception("❌ Could not connect to database after retries")
