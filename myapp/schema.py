from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    mobile_no: str
    email: EmailStr
    password: str  # Add password field

class UserUpdate(BaseModel):
    name: Optional[str]
    mobile_no: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]  # Add password field

class UserOut(BaseModel):
    id: int
    name: str
    mobile_no: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class DiscussionCreate(BaseModel):
    text: str
    hashtags: List[str]

class DiscussionUpdate(BaseModel):
    text: Optional[str]
    image: Optional[str]
    hashtags: Optional[List[str]]

class DiscussionOut(BaseModel):
    id: int
    text: str
    hashtags: List[str]
    image: Optional[str]
    created_on: datetime
    view_count: Optional[int]

class CommentCreate(BaseModel):
    text: str
    discussion_id: int

class CommentOut(BaseModel):
    id: int
    text: str
    created_on: datetime
    user: UserOut

    class Config:
        orm_mode = True

class LikeOut(BaseModel):
    id: int
    created_on: datetime
    user: UserOut

    class Config:
        orm_mode = True

class LoginData(BaseModel):
    email: EmailStr
    password: str
