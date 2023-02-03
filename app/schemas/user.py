from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool] = True
    is_admin: bool = False


class User(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    email: EmailStr
    password: str
