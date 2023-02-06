from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config import settings
from app.db.db_session import get_session
from app.routers.hashing import create_access_token
from app.routers.utils import authenticate_user
from app.schemas.token import Token

router = APIRouter()


@router.post("/", response_model=Token)
def singin_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"inf": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
