from fastapi import APIRouter
from pydantic import BaseModel

from services.ai.factory import get_ai_provider

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str


@router.post("")
def chat(req: ChatRequest):
    provider = get_ai_provider()
    reply = provider.chat(req.message)

    return {
        "user": req.message,
        "assistant": reply,
    }
