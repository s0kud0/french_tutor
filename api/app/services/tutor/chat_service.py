from fastapi import HTTPException
from sqlmodel import Session as DBSession, select

from models.chat import LearningNote, Message, Session as ChatSession
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
    if not history and chat_session.title == "New practice":
        chat_session.title = _build_session_title(message, mode)
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)

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
    _save_learning_notes(db, chat_session.id, reply)

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


def _build_session_title(message: str, mode: str) -> str:
    normalized_message = message.lower()
    for phrase in [
        "i want to practice ",
        "i would like to practice ",
        "let's practice ",
        "lets practice ",
        "practice ",
    ]:
        if normalized_message.startswith(phrase):
            message = message[len(phrase):]
            break

    words = [
        word.strip(".,!?;:()[]{}\"'")
        for word in message.split()
        if word.strip(".,!?;:()[]{}\"'")
    ]
    title_text = " ".join(words[:5])
    if not title_text:
        title_text = mode.capitalize()

    if len(words) > 5:
        title_text = f"{title_text}..."

    return title_text[:60]


def _save_learning_notes(db: DBSession, session_id: int, assistant_reply: str):
    notes = _extract_learning_notes(assistant_reply)
    for note in notes:
        db.add(
            LearningNote(
                session_id=session_id,
                category=note["category"],
                content=note["content"],
            )
        )

    if notes:
        db.commit()


def _extract_learning_notes(assistant_reply: str) -> list[dict[str, str]]:
    notes = []
    for line in assistant_reply.splitlines():
        content = line.strip(" -*")
        lowered = content.lower()

        if not content or len(content) < 12:
            continue

        if any(keyword in lowered for keyword in ["correction", "corrected", "natural"]):
            notes.append({"category": "Correction", "content": content})
        elif any(keyword in lowered for keyword in ["vocabulary", "phrase", "expression"]):
            notes.append({"category": "Vocabulary", "content": content})
        elif any(keyword in lowered for keyword in ["grammar", "tense", "conjugat"]):
            notes.append({"category": "Grammar", "content": content})

        if len(notes) >= 3:
            break

    return notes
