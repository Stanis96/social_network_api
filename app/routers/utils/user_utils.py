from typing import Any
from typing import List
from typing import Optional

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose import jwt
from sqlalchemy import exc
from sqlalchemy.orm import Session

from app import models
from app import schemas
from app.config import settings
from app.db.db_session import get_session
from app.routers.utils.hashing import Hasher


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/singin")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)
) -> Any:
    data_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate data",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]  # type:ignore
        )
        username: Optional[Any] = payload.get("sub")
        if username is None:
            raise data_exception
    except JWTError:
        raise data_exception
    user = UserService(db).get_user(username=username)
    if user is None:
        raise data_exception
    return user


class UserService:
    def __init__(self, db: Session = Depends(get_session)) -> None:
        self.db = db

    def create_new_user(self, user: schemas.UserCreate) -> models.User:
        db_user = models.User(
            username=user.username,
            email=user.email,
            hashed_password=Hasher.get_password_hash(user.password),
            is_active=True,
            is_admin=False,
        )
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
        except exc.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="This email address already exists"
            )
        return db_user

    def get_user(self, username: str) -> Any:
        user = self.db.query(models.User).filter(models.User.email == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{username} not found!"
            )
        return user

    def get_user_email(self, email: Optional[str]) -> Any:
        user = self.db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{email} not found!")
        return user

    def get_all_users(self) -> List[models.User]:
        users = self.db.query(models.User).filter(models.User.is_active == True).all()
        return users

    def authenticate_user(self, username: str, password: str) -> Any:
        user = self.get_user(username=username)
        if not user:
            return False
        if not Hasher.validate_password(password, user.hashed_password):
            return False
        return user
