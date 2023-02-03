from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate

from .hashing import Hasher


def create_user(user: UserCreate, db: Session) -> User:
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
