from fastapi import APIRouter, Depends
from sqlmodel import Session as DBSession, select

from core.database import get_session
from models.chat import Session

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("")
def create_session(session: DBSession = Depends(get_session)):
    new_session = Session()
    session.add(new_session)
    session.commit()
    session.refresh(new_session)
    return new_session


@router.get("")
def list_sessions(session: DBSession = Depends(get_session)):
    result = session.exec(select(Session)).all()
    return result


@router.get("/{session_id}")
def get_session(session_id: int, session: DBSession = Depends(get_session)):
    result = session.get(Session, session_id)
    return result
