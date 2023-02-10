from sqlalchemy.orm import Session

from app import models
from app import schemas


def create_new_post(post: schemas.PostCreate, db: Session, user_id: int) -> schemas.Post:
    post_object = models.Post(**post.dict(), user_id=user_id)
    db.add(post_object)
    db.commit()
    db.refresh(post_object)
    return post_object
