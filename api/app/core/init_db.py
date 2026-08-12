import time
from sqlmodel import SQLModel
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from core.database import engine
from models.chat import LearningNote, Message, Session


def init_db(retries: int = 10, delay: float = 2.0):
    print("🚀 Initializing database...")

    for i in range(retries):
        try:
            SQLModel.metadata.create_all(engine)
            _upgrade_existing_tables()
            print("✅ Database tables created successfully")
            return
        except OperationalError as e:
            print(f"⏳ DB not ready yet (attempt {i+1}/{retries})...")
            time.sleep(delay)

    raise Exception("❌ Could not connect to database after retries")


def _upgrade_existing_tables():
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                ALTER TABLE "session"
                ADD COLUMN IF NOT EXISTS title VARCHAR NOT NULL DEFAULT 'New practice'
                """
            )
        )
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS learningnote (
                    id SERIAL NOT NULL,
                    session_id INTEGER NOT NULL,
                    category VARCHAR NOT NULL,
                    content VARCHAR NOT NULL,
                    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                    PRIMARY KEY (id)
                )
                """
            )
        )
        connection.execute(
            text(
                """
                CREATE INDEX IF NOT EXISTS ix_learningnote_session_id
                ON learningnote (session_id)
                """
            )
        )
