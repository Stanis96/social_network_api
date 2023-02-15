from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Depends

from app import schemas
from app.routers.utils.post_utils import PostService
from app.routers.utils.user_utils import get_current_user


router = APIRouter()


@router.post("/create", response_model=schemas.Post, status_code=200)
def create_post(
    post: schemas.PostCreate,
    post_tools: PostService = Depends(),
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    """
    Access is provided after authorization.
    Create a new post.
    """
    post = post_tools.create_new_post(post, user_id=current_user.id)
    return post


@router.get("/show_all", response_model=List[schemas.PostShow], status_code=200)
def show_posts(
    post_tools: PostService = Depends(), current_user: schemas.User = Depends(get_current_user)
) -> List[schemas.PostShow]:
    """
    Access is provided after authorization.
    Providing data about all created posts.
    """
    posts = post_tools.get_all_posts()
    return posts


@router.get("/show/{post_id}", response_model=schemas.PostShow, status_code=200)
def show_post(
    post_id: int,
    post_tools: PostService = Depends(),
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    """
    Access is provided after authorization.
    Search current post by id and check existing id.
    """
    post = post_tools._get_current_post(post_id)
    return post


@router.put("/update/{post_id}", response_model=schemas.PostShow, status_code=200)
def update_post(
    *,
    post_id: int,
    post_tools: PostService = Depends(),
    current_user: schemas.User = Depends(get_current_user),
    existing_post: schemas.PostUpdate,
) -> Any:
    """
    Access is provided after authorization.
    Update only own posts.
    """
    post = post_tools.update_current_post(
        post_id, user_id=current_user.id, existing_post=existing_post
    )
    return post


@router.delete("/delete/{post_id}", status_code=200)
def delete_post(
    post_id: int,
    post_tools: PostService = Depends(),
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    """
    Access is provided after authorization.
    Delete only own posts.
    """
    post = post_tools.delete_current_post(post_id, user_id=current_user.id)
    return post


@router.post("/like/{post_id}", response_model=schemas.PostShow, status_code=200)
def like_post(
    post_id: int,
    post_tools: PostService = Depends(),
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    """
    Access is provided after authorization.
    Unable to like own post.
    Available to like a post but put it again and the like will be deleted or
    dislike the post and the like will also be deleted.
    """
    post = post_tools.add_like(post_id, user_id=current_user.id)
    return post


@router.post("/dislike/{post_id}", response_model=schemas.PostShow, status_code=200)
def dislike_post(
    post_id: int,
    post_tools: PostService = Depends(),
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    """
    Access is provided after authorization.
    Unable to dislike own post.
    Available to dislike a post but put it again and the dislike will be deleted or
    like the post and the dislike will also be deleted.
    """

    post = post_tools.add_dislike(post_id, user_id=current_user.id)
    return post
