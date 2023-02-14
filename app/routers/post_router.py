from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app import schemas
from app.db.db_session import get_session
from app.routers.utils.post_utils import add_dislike
from app.routers.utils.post_utils import add_like
from app.routers.utils.post_utils import create_new_post
from app.routers.utils.post_utils import delete_current_post
from app.routers.utils.post_utils import get_all_posts
from app.routers.utils.post_utils import get_current_post
from app.routers.utils.post_utils import update_current_post
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


@router.get("/show/{post_id}", response_model=schemas.PostShow)
def show_post(
    post_id: int,
    db: Session = Depends(get_session),
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    return get_current_post(post_id=post_id, db=db)


@router.put("/update/{post_id}", response_model=schemas.PostShow)
def update_post(
    *,
    post_id: int,
    db: Session = Depends(get_session),
    current_user: schemas.User = Depends(get_current_user),
    existing_post: schemas.PostUpdate,
):
    return update_current_post(
        post_id=post_id, user_id=current_user.id, db=db, existing_post=existing_post
    )


@router.delete("/delete/{post_id}", status_code=200)
def delete_post(
    post_id: int,
    db: Session = Depends(get_session),
    current_user: schemas.User = Depends(get_current_user),
):
    return delete_current_post(post_id=post_id, db=db, user_id=current_user.id)


@router.post("/like/{post_id}", status_code=200, response_model=schemas.PostShow)
def like_post(
    post_id: int,
    db: Session = Depends(get_session),
    current_user: schemas.User = Depends(get_current_user),
):
    return add_like(post_id=post_id, user_id=current_user.id, db=db)


@router.post("/dislike/{post_id}", status_code=200, response_model=schemas.PostShow)
def dislike_post(
    post_id: int,
    db: Session = Depends(get_session),
    current_user: schemas.User = Depends(get_current_user),
):
    return add_dislike(post_id=post_id, user_id=current_user.id, db=db)
