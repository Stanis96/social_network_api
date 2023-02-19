from fastapi import Depends
from fastapi.testclient import TestClient

from app import schemas
from app.routers.utils.user_utils import UserService


def user_authentication(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    r = client.post("/singin/", data=data)
    response = r.json()
    auth_token = response["access_token"]
    header = {"Authorization": f"bearer {auth_token}"}
    return header


def authentication_token(client: TestClient, email: str, user_tools: UserService = Depends()):
    password = "creative_password"
    user = user_tools.get_user_email(email=email)
    if not user:
        user_in_create = schemas.UserCreate(username=email, email=email, password=password)
        user = user_tools.create_new_user(user=user_in_create)
    return user_authentication(client=client, email=email, password=password)
