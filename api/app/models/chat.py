from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(default="New practice")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(index=True)

    role: str
    content: str

    created_at: datetime = Field(default_factory=datetime.utcnow)


class LearningNote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(index=True)

    category: str
    content: str

    created_at: datetime = Field(default_factory=datetime.utcnow)
