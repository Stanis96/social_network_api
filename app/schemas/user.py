from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr]
    is_active: Optional[bool] = True
    is_admin: bool = False


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    email: EmailStr
    password: str
