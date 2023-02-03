from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.db_session import get_session
from app.schemas import user

from .utils import create_user

router = APIRouter()


@router.post("/", response_model=user.User)
def create_user(user: user.UserCreate, db: Session = Depends(get_session)):
    return create_user(user=user, db=db)
