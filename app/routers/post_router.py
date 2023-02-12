from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app import schemas
from app.db.db_session import get_session
from app.routers.utils.post_utils import create_new_post
from app.routers.utils.post_utils import get_all_posts
from app.routers.utils.post_utils import get_current_post
from app.routers.utils.user_utils import get_current_user


router = APIRouter()


@router.post("/create", response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_session),
    current_user: schemas.User = Depends(get_current_user),
):
    post = create_new_post(post=post, db=db, user_id=current_user.id)
    return post


@router.get("/show_all", response_model=List[schemas.PostShow])
def show_posts(
    db: Session = Depends(get_session), current_user: schemas.User = Depends(get_current_user)
) -> List[schemas.PostShow]:
    return get_all_posts(db=db)


@router.get("/show_post/{id}", response_model=schemas.PostShow)
def show_post(
    post_id: int,
    db: Session = Depends(get_session),
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    return get_current_post(post_id=post_id, db=db)
