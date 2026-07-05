from fastapi import APIRouter, Depends
from sqlmodel import Session as DBSession, select

from core.database import get_session
from models.chat import Message

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("")
def create_message(message: Message, session: DBSession = Depends(get_session)):
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


@router.get("/{session_id}")
def get_messages(session_id: int, session: DBSession = Depends(get_session)):
    result = session.exec(
        select(Message).where(Message.session_id == session_id)
    ).all()
    return result
