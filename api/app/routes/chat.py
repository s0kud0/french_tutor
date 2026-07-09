from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session as DBSession

from core.database import get_session
from services.ai.factory import get_ai_provider
from services.tutor.chat_service import handle_tutor_chat

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    session_id: int | None = None
    level: str = "beginner"
    mode: str = "conversation"


@router.post("")
def chat(req: ChatRequest, session: DBSession = Depends(get_session)):
    provider = get_ai_provider()

    return handle_tutor_chat(
        db=session,
        provider=provider,
        message=req.message,
        session_id=req.session_id,
        level=req.level,
        mode=req.mode,
    )
