from typing import Dict, List

from fastapi import WebSocket, WebSocketDisconnect
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .auth import SECRET_KEY, ALGORITHM
from . import crud


class ConnectionManager:
    def __init__(self):
        self._rooms: Dict[int, List[WebSocket]] = {}
        self._user_map: Dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, room_id: int, username: str):
        await websocket.accept()
        self._rooms.setdefault(room_id, []).append(websocket)
        self._user_map[websocket] = username

    def disconnect(self, websocket: WebSocket, room_id: int):
        self._rooms.get(room_id, []).remove(websocket) if websocket in self._rooms.get(
            room_id, []
        ) else None
        self._user_map.pop(websocket, None)

    async def broadcast(self, payload: dict, room_id: int):
        for ws in list(self._rooms.get(room_id, [])):
            try:
                await ws.send_json(payload)
            except Exception:
                pass

    def active_users(self, room_id: int) -> List[str]:
        return [self._user_map[ws] for ws in self._rooms.get(room_id, []) if ws in self._user_map]


manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket, room_id: int, db: Session):
    token = websocket.query_params.get("token")
    username = "anonymous"
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("username", "anonymous")
        except JWTError:
            await websocket.close(code=4001)
            return

    await manager.connect(websocket, room_id, username)
    await manager.broadcast({"type": "join", "username": username}, room_id)

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type", "message")

            if msg_type == "message":
                content = data.get("content", "").strip()
                if content:
                    user = crud.get_user_by_username(db, username)
                    if user:
                        msg = crud.create_message(db, content, user.id, room_id)
                        await manager.broadcast(
                            {
                                "type": "message",
                                "id": msg.id,
                                "content": msg.content,
                                "username": username,
                                "timestamp": msg.timestamp.isoformat(),
                                "room_id": room_id,
                            },
                            room_id,
                        )
            elif msg_type == "typing":
                await manager.broadcast({"type": "typing", "username": username}, room_id)
            elif msg_type == "stop_typing":
                await manager.broadcast({"type": "stop_typing", "username": username}, room_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        await manager.broadcast({"type": "leave", "username": username}, room_id)
