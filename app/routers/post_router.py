from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app import schemas
from app.db.db_session import get_session
from app.routers.utils.post_utils import create_new_post
from app.routers.utils.user_utils import get_current_user


router = APIRouter()


@router.post("/create", response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_session),
    current_user: schemas.User = Depends(get_current_user),
) -> Optional[schemas.Post]:
    post = create_new_post(post=post, db=db, user_id=current_user.id)
    return post
