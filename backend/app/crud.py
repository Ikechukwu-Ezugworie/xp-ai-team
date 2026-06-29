from sqlalchemy.orm import Session
from . import models, schemas


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    pass  # TODO: - implement


def get_rooms(db: Session):
    return db.query(models.Room).all()


def create_room(db: Session, room: schemas.RoomBase):
    pass  # TODO: implement


def get_messages(db: Session, room_id: int, limit: int = 50):
    return (
        db.query(models.Message)
        .filter(models.Message.room_id == room_id)
        .limit(limit)
        .all()
    )


def create_message(
    db: Session, message: schemas.MessageBase, user_id: int, room_id: int
):
    pass  # TODO: implement
