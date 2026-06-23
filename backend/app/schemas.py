from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class MessageBase(BaseModel):
    content: str

class RoomBase(BaseModel):
    name: str