from datetime import timedelta
from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import settings
from app.routers.utils.hashing import create_access_token
from app.routers.utils.user_utils import UserService
from app.schemas.token import Token


router = APIRouter()


@router.post("/", response_model=Token, status_code=200)
def singin_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), user_tools: UserService = Depends()
) -> Any:
    """
    Providing access token OAuth2.
    """
    user = user_tools.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
