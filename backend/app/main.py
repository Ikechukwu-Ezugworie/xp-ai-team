import os

from fastapi import FastAPI, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import Base
from .routers import auth, messages, rooms
from .websocket import websocket_endpoint

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chat App Backend", version="1.0.0")

_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])


@app.websocket("/ws/{room_id}")
async def ws_route(websocket: WebSocket, room_id: int, db: Session = Depends(get_db)):
    await websocket_endpoint(websocket, room_id, db)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "chat-backend"}
