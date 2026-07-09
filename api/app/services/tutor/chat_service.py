from fastapi import HTTPException
from sqlmodel import Session as DBSession, select

from models.chat import Message, Session as ChatSession
from services.ai.base import AIProvider
from services.tutor.prompts import build_tutor_prompt


def handle_tutor_chat(
    db: DBSession,
    provider: AIProvider,
    message: str,
    session_id: int | None = None,
    level: str = "beginner",
    mode: str = "conversation",
) -> dict:
    chat_session = _get_or_create_session(db, session_id)
    history = _get_recent_messages(db, chat_session.id)

    user_message = Message(
        session_id=chat_session.id,
        role="user",
        content=message,
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    prompt = build_tutor_prompt(
        message=message,
        history=history,
        level=level,
        mode=mode,
    )
    reply = provider.chat(prompt)

    assistant_message = Message(
        session_id=chat_session.id,
        role="assistant",
        content=reply,
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return {
        "session_id": chat_session.id,
        "user": user_message,
        "assistant": assistant_message,
    }


def _get_or_create_session(
    db: DBSession,
    session_id: int | None,
) -> ChatSession:
    if session_id is None:
        chat_session = ChatSession()
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)
        return chat_session

    chat_session = db.get(ChatSession, session_id)
    if chat_session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return chat_session


def _get_recent_messages(
    db: DBSession,
    session_id: int,
    limit: int = 12,
) -> list[Message]:
    statement = (
        select(Message)
        .where(Message.session_id == session_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    messages = db.exec(statement).all()
    return list(reversed(messages))
