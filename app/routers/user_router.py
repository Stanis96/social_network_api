from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app import schemas
from app.db.db_session import get_session

from .utils import create_new_user
from .utils import get_all_users
from .utils import get_current_user


router = APIRouter()


@router.post("/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_session)):
    user = create_new_user(user=user, db=db)
    return user


@router.get("/show_all", response_model=List[schemas.User])
def show_users(
    db: Session = Depends(get_session), current_user: schemas.User = Depends(get_current_user)
) -> list[schemas.User]:
    return get_all_users(db=db)
