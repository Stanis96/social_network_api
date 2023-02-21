from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import schemas
from app.routers.utils.user_utils import UserService


def user_authentication(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    r = client.post("/singin/", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"bearer {auth_token}"}
    return headers


def authentication_token(*, client: TestClient, email: str, db: Session):
    password = "password1"
    user = UserService(db).get_user_email(email=email)
    if not user:
        user_in_create = schemas.UserCreate(username=email, email=email, password=password)
        user = UserService(db).create_new_user(user=user_in_create)
    return user_authentication(client=client, email=email, password=password)
