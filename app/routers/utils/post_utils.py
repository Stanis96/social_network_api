from typing import Any
from typing import List

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app import models
from app import schemas


def create_new_post(post: schemas.PostCreate, db: Session, user_id: int) -> schemas.Post:
    post_object = models.Post(**post.dict(), user_id=user_id)
    db.add(post_object)
    db.commit()
    db.refresh(post_object)
    return post_object


def get_post_info(
    posts: models.Post, count_likes: int = 0, count_dislikes: int = 0
) -> schemas.PostShow:
    return schemas.PostShow(
        id=posts.id,
        owner_id=posts.user_id,
        title=posts.title,
        content=posts.content,
        date_creation=posts.date_creation,
        likes=count_likes,
        dislikes=count_dislikes,
    )


def get_all_posts(db: Session) -> List[schemas.PostShow]:
    posts: list = db.query(models.Post).all()
    posts = [get_post_info(post, post.count_likes(), post.count_dislikes()) for post in posts]
    return posts


def get_current_post(post_id: int, db: Session) -> Any:
    post_query = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {post_id} didn't find",
        )
    post = get_post_info(post_query, post_query.count_likes(), post_query.count_dislikes())
    return post
