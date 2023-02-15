from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Depends

from app import models
from app import schemas
from app.routers.utils.user_utils import UserService
from app.routers.utils.user_utils import get_current_user


router = APIRouter()


@router.post("/create", response_model=schemas.User, status_code=200)
def create_user(user: schemas.UserCreate, user_tools: UserService = Depends()) -> Any:
    """
    Creation a user when using a unique email address.
    """
    user = user_tools.create_new_user(user)
    return user


@router.get("/show_all", response_model=List[schemas.User], status_code=200)
def show_users(
    user_tools: UserService = Depends(), current_user: schemas.User = Depends(get_current_user)
) -> Any:
    """
    Access is provided after authorization.
    Providing data about all created users.
    """
    users = user_tools.get_all_users()
    return users


@router.get("/show_user", response_model=schemas.User, status_code=200)
def show_myself(current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Access is provided after authorization.
    Providing your user data.
    """
    return current_user


@router.get("/{email}", response_model=schemas.User, status_code=200)
def find_user_by_email(
    user_tools: UserService = Depends(),
    current_user: models.User = Depends(get_current_user),
    email: str = None,
) -> Any:
    """
    Access is provided after authorization.
    Search current user by email and check existing email.
    """
    user = user_tools.get_user_email(email=email)
    return user
