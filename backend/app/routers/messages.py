from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..auth import get_current_user
from ..database import get_db
from ..models import User

router = APIRouter()


def _msg_to_schema(msg) -> schemas.MessageResponse:
    return schemas.MessageResponse(
        id=msg.id,
        content=msg.content,
        user_id=msg.user_id,
        room_id=msg.room_id,
        timestamp=msg.timestamp,
        username=msg.user.username if msg.user else "unknown",
    )


@router.get("/{room_id}", response_model=List[schemas.MessageResponse])
def get_messages(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not crud.get_room(db, room_id):
        raise HTTPException(status_code=404, detail="Room not found")
    return [_msg_to_schema(m) for m in crud.get_messages(db, room_id)]


@router.post("/{room_id}", response_model=schemas.MessageResponse, status_code=201)
def send_message(
    room_id: int,
    body: schemas.MessageBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not crud.get_room(db, room_id):
        raise HTTPException(status_code=404, detail="Room not found")
    msg = crud.create_message(db, body.content, current_user.id, room_id)
    return _msg_to_schema(msg)


@router.get("/{room_id}/search", response_model=schemas.SearchResult)
def search_messages(
    room_id: int,
    q: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not crud.get_room(db, room_id):
        raise HTTPException(status_code=404, detail="Room not found")
    results = crud.search_messages(db, room_id, q)
    msgs = [_msg_to_schema(m) for m in results]
    return schemas.SearchResult(messages=msgs, total=len(msgs))
