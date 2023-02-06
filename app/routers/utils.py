from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import models, schemas
from app.config import settings
from app.db.db_session import get_session

from .hashing import Hasher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/singin")


def create_new_user(user: schemas.UserCreate, db: Session) -> schemas.User:
    user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=True,
        is_admin=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(username: str, db: Session) -> Optional[schemas.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_email(email: str, db: Session) -> Optional[schemas.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_all_users(self) -> list[schemas.User]:
    users = self.session.query(models.User).where(models.User.is_active == True).all()

    if not users:
        return list()
    return [schemas.User.from_orm(user) for user in users]


def authenticate_user(email: str, password: str, db: Session = Depends(get_session)):
    user = get_user_email(email=email, db=db)
    print(user)
    if not user:
        return False
    if not Hasher.validate_password(password, models.User.hashed_password):
        return False
    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    data_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate data",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("inf")
        print("username/email from ", username)
        if username is None:
            raise data_exception
    except JWTError:
        raise data_exception
    user = get_user(username=username, db=db)
    if user is None:
        raise data_exception
    return user
