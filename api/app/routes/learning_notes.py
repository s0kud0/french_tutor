from fastapi import APIRouter, Depends
from sqlmodel import Session as DBSession, select

from core.database import get_session
from models.chat import LearningNote

router = APIRouter(prefix="/learning-notes", tags=["learning notes"])


@router.get("/{session_id}")
def get_learning_notes(session_id: int, session: DBSession = Depends(get_session)):
    statement = (
        select(LearningNote)
        .where(LearningNote.session_id == session_id)
        .order_by(LearningNote.created_at.desc())
    )
    return session.exec(statement).all()
