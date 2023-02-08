from typing import Any
from typing import List
from typing import Optional

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose import jwt
from sqlalchemy.orm import Session

from app import models
from app import schemas
from app.config import settings
from app.db.db_session import get_session

from .hashing import Hasher


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/singin")


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
    return db.query(models.User).filter(models.User.email == username).first()


def get_all_users(db: Session) -> List[schemas.User]:
    return db.query(models.User).filter(models.User.is_active == True).all()


def authenticate_user(username: str, password: str, db: Session = Depends(get_session)):
    user = get_user(username=username, db=db)
    print(user)
    if not user:
        return False
    if not Hasher.validate_password(password, user.hashed_password):
        return False
    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    data_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate data",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: Optional[Any] = payload.get("sub")
        print("username/email from ", username)
        if username is None:
            raise data_exception
    except JWTError:
        raise data_exception
    user = get_user(username=username, db=db)
    if user is None:
        raise data_exception
    return user
