from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app import models
from app import schemas
from app.db.db_session import get_session
from app.routers.utils.user_utils import create_new_user
from app.routers.utils.user_utils import get_all_users
from app.routers.utils.user_utils import get_current_user
from app.routers.utils.user_utils import get_user_email


router = APIRouter()


@router.post("/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_session)):
    user = create_new_user(user=user, db=db)
    return user


@router.get("/show_all", response_model=List[schemas.User])
def show_users(
    db: Session = Depends(get_session), current_user: schemas.User = Depends(get_current_user)
) -> Any:
    return get_all_users(db=db)


@router.get("/show_user", response_model=schemas.User)
def show_myself(
    db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)
) -> Any:
    return current_user


@router.get("/{email}", response_model=schemas.User)
def find_user_by_email(
    db: Session = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
    email: str = None,
) -> Any:
    return get_user_email(email=email, db=db)
