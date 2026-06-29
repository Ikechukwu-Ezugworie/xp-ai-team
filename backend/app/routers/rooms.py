from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..auth import get_current_user
from ..database import get_db
from ..models import Room, User

router = APIRouter()


@router.get("/", response_model=List[schemas.RoomResponse])
def list_rooms(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rooms = crud.get_rooms(db)
    return [
        schemas.RoomResponse(
            id=r.id, name=r.name, created_at=r.created_at, member_count=len(r.members)
        )
        for r in rooms
    ]


@router.post("/", response_model=schemas.RoomResponse, status_code=201)
def create_room(
    room: schemas.RoomBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if db.query(Room).filter(Room.name == room.name).first():
        raise HTTPException(status_code=400, detail="Room name already exists")
    db_room = crud.create_room(db, room)
    crud.join_room(db, db_room.id, current_user.id)
    db.refresh(db_room)
    return schemas.RoomResponse(
        id=db_room.id, name=db_room.name, created_at=db_room.created_at,
        member_count=len(db_room.members),
    )


@router.post("/{room_id}/join", response_model=schemas.RoomResponse)
def join_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    room = crud.get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    crud.join_room(db, room_id, current_user.id)
    db.refresh(room)
    return schemas.RoomResponse(
        id=room.id, name=room.name, created_at=room.created_at, member_count=len(room.members)
    )


@router.post("/{room_id}/leave")
def leave_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    room = crud.get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    crud.leave_room(db, room_id, current_user.id)
    return {"message": "Left room"}


@router.get("/{room_id}/members", response_model=List[schemas.MemberResponse])
def get_members(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    room = crud.get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    members = crud.get_room_members(db, room_id)
    return [schemas.MemberResponse(user_id=m.user_id, username=m.user.username) for m in members]


@router.delete("/{room_id}", status_code=204)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    room = crud.get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    crud.delete_room(db, room_id)
