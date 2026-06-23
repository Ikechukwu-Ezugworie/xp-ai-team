from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, messages, rooms
from .websocket import websocket_endpoint

app = FastAPI(title="Chat App Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
app.include_router(rooms.router, prefix="/rooms", tags=["rooms"])

@app.websocket("/ws")
async def websocket_route(websocket):
    await websocket_endpoint(websocket)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "chat-backend"}                  