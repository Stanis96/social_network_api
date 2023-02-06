from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.db.db_session import get_session

from .utils import create_new_user, get_all_users

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_session)):
    user = create_new_user(user=user, db=db)
    return user


@router.get("/", response_model=List[schemas.User])
def show_users(
    db: Session = Depends(get_session), current_user: schemas.User = Depends(get_all_users)
) -> list[schemas.User]:
    return get_all_users()
