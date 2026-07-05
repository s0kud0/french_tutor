from fastapi import FastAPI
from core.init_db import init_db
from routes import sessions, messages, chat
from routes.sessions import router as sessions_router
from routes.messages import router as messages_router
from routes.chat import router as chat_router

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

app.include_router(sessions_router)
app.include_router(messages_router)
app.include_router(chat_router)

@app.get("/health")
def health():
    return {"status": "ok"}
