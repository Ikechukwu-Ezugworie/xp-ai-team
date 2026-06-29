from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str


class RoomBase(BaseModel):
    name: str


class RoomResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    member_count: Optional[int] = 0

    model_config = {"from_attributes": True}


class MemberResponse(BaseModel):
    user_id: int
    username: str

    model_config = {"from_attributes": True}


class MessageBase(BaseModel):
    content: str


class MessageResponse(BaseModel):
    id: int
    content: str
    user_id: int
    room_id: int
    timestamp: datetime
    username: str

    model_config = {"from_attributes": True}


class SearchResult(BaseModel):
    messages: List[MessageResponse]
    total: int
