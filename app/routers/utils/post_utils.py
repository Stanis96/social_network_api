from typing import Any
from typing import List

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy import exc
from sqlalchemy.orm import Session

from app import models
from app import schemas
from app.db.db_session import get_session


class PostService:
    def __init__(self, db: Session = Depends(get_session)) -> None:
        self.db = db

    def create_new_post(self, post: schemas.PostCreate, user_id: int) -> models.Post:
        post_object = models.Post(**post.dict(), user_id=user_id)
        self.db.add(post_object)
        self.db.commit()
        self.db.refresh(post_object)
        return post_object

    def _get_current_post(self, post_id: int) -> Any:
        post = self.db.query(models.Post).filter(models.Post.id == post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The post {post_id} not found",
            )
        return post

    def _get_user_by_id(self, user_id: int) -> Any:
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        return user

    def get_all_posts(self) -> List[schemas.PostShow]:
        posts: list = self.db.query(models.Post).all()
        return posts

    def update_current_post(self, post_id: int, user_id: int, existing_post) -> Any:
        post = self._get_current_post(post_id=post_id)
        if post.user_id == user_id:
            post.title = existing_post.title
            post.content = existing_post.content
            self.db.add(post)
            self.db.commit()
            return post
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"The {post_id} not valid for update"
        )

    def delete_current_post(self, post_id: int, user_id: int):
        post = self._get_current_post(post_id=post_id)

        if post.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"The {post_id} not valid for delete"
            )

        if post.user_id == user_id:
            self.db.delete(post)
            self.db.commit()
            return post

    def add_like(self, post_id: int, user_id: int):
        post = self._get_current_post(post_id=post_id)
        user = self._get_user_by_id(user_id=user_id)

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
            self.db.commit()
            self.db.add(post)
        except exc.IntegrityError:
            self.db.rollback()
        return post

    def add_dislike(self, post_id: int, user_id: int):
        post = self._get_current_post(post_id=post_id)
        user = self._get_user_by_id(user_id=user_id)

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
            self.db.commit()
            self.db.add(post)
        except exc.IntegrityError:
            self.db.rollback()

        return post
