from typing import Any
from typing import List

from fastapi import HTTPException
from fastapi import status
from sqlalchemy import exc
from sqlalchemy.orm import Session

from app import models
from app import schemas


def create_new_post(post: schemas.PostCreate, db: Session, user_id: int) -> schemas.Post:
    post_object = models.Post(**post.dict(), user_id=user_id)
    db.add(post_object)
    db.commit()
    db.refresh(post_object)
    return post_object


def get_all_posts(db: Session) -> List[schemas.PostShow]:
    posts: list = db.query(models.Post).all()
    return posts


def get_current_post(post_id: int, db: Session) -> Any:
    post_query = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {post_id} didn't find",
        )
    return post_query


def update_current_post(post_id: int, user_id: int, db: Session, existing_post):
    post = (
        db.query(models.Post).filter(models.Post.id == post_id).first()
    )  # optimization get_current_post
    if post.user_id == user_id:
        post.title = existing_post.title
        post.content = existing_post.content
        db.add(post)
        db.commit()
        return post


def delete_current_post(post_id: int, user_id: int, db: Session):
    post = (
        db.query(models.Post).filter(models.Post.id == post_id).first()
    )  # optimization get_current_post
    if post.user_id == user_id:
        db.delete(post)
        db.commit()
        return post


def add_like(post_id: int, user_id: int, db: Session):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user_id == post.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You cannot like your post"
        )

    if user in post.likes:
        post.likes.remove(user)
        post.likes_count -= 1

    else:
        post.likes.append(user)
        post.likes_count += 1

        if user in post.dislikes:
            post.dislikes.remove(user)
            post.dislikes_count -= 1

    try:
        db.commit()
        db.add(post)
    except exc.IntegrityError:
        db.rollback()
    return post


def add_dislike(post_id: int, user_id: int, db: Session):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user_id == post.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You cannot dislike your post"
        )

    if user in post.dislikes:
        post.dislikes.remove(user)
        post.dislikes_count -= 1

    else:
        post.dislikes.append(user)
        post.dislikes_count += 1

        if user in post.likes:
            post.likes.remove(user)
            post.likes_count -= 1

    try:
        db.commit()
        db.add(post)
    except exc.IntegrityError:
        db.rollback()

    return post
