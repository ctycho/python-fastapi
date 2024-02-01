from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr


@dataclass
class ValueRange:
    """range values"""
    lo: int
    hi: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime 

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    """Post"""
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    """post create"""


class Post(PostBase):
    """post response"""
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None

    class Config:
        from_attributes = True


class Vote(BaseModel):
    post_id: int
    dir: int
