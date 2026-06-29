from sqlalchemy.orm import Session

from . import models, schemas
from .auth import hash_password


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_rooms(db: Session):
    rooms = db.query(models.Room).all()
    for room in rooms:
        room.member_count = len(room.members)
    return rooms


def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()


def create_room(db: Session, room: schemas.RoomBase):
    db_room = models.Room(name=room.name)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def delete_room(db: Session, room_id: int):
    room = get_room(db, room_id)
    if room:
        db.delete(room)
        db.commit()
    return room


def get_room_member(db: Session, room_id: int, user_id: int):
    return (
        db.query(models.RoomMember)
        .filter(
            models.RoomMember.room_id == room_id,
            models.RoomMember.user_id == user_id,
        )
        .first()
    )


def join_room(db: Session, room_id: int, user_id: int):
    if get_room_member(db, room_id, user_id):
        return None
    member = models.RoomMember(room_id=room_id, user_id=user_id)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def leave_room(db: Session, room_id: int, user_id: int):
    member = get_room_member(db, room_id, user_id)
    if member:
        db.delete(member)
        db.commit()
    return member


def get_room_members(db: Session, room_id: int):
    return (
        db.query(models.RoomMember)
        .filter(models.RoomMember.room_id == room_id)
        .all()
    )


def get_messages(db: Session, room_id: int, limit: int = 50):
    return (
        db.query(models.Message)
        .filter(models.Message.room_id == room_id)
        .order_by(models.Message.timestamp.asc())
        .limit(limit)
        .all()
    )


def create_message(db: Session, content: str, user_id: int, room_id: int):
    msg = models.Message(content=content, user_id=user_id, room_id=room_id)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    db.refresh(msg, attribute_names=["user"])
    return msg


def search_messages(db: Session, room_id: int, query: str):
    return (
        db.query(models.Message)
        .filter(
            models.Message.room_id == room_id,
            models.Message.content.ilike(f"%{query}%"),
        )
        .order_by(models.Message.timestamp.asc())
        .all()
    )
