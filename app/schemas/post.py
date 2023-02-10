from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Post(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    date_creation: datetime

    class Config:
        orm_mode = True


class PostShow(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    date_creation: datetime
    likes: int
    dislikes: int

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    title: Optional[str]
    content: Optional[str]


class PostUpdate(PostCreate):
    pass
