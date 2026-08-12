from fastapi import FastAPI
from core.init_db import init_db
from routes import chat, learning_notes, messages, sessions
from routes.sessions import router as sessions_router
from routes.messages import router as messages_router
from routes.chat import router as chat_router
from routes.learning_notes import router as learning_notes_router

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

app.include_router(sessions_router)
app.include_router(messages_router)
app.include_router(chat_router)
app.include_router(learning_notes_router)

@app.get("/health")
def health():
    return {"status": "ok"}
