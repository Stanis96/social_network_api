from typing import Any

from fastapi import status

from app.config import settings


"""Tests for user routers."""


def test_create_user(client: Any) -> None:
    data1 = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password1",
    }
    response = client.post("/users/create", json=data1)
    assert response.status_code == 200
    assert response.json()["email"] == settings.TEST_USER_EMAIL
    assert response.json()["is_active"] == True
    assert response.json()["is_admin"] == False


def test_show_users(client: Any, normal_user_token: dict[str, str]) -> None:
    data2 = {
        "username": "testuser2",
        "email": "testuser2@example.com",
        "password": "password2",
    }
    data3 = {
        "username": "testuser3",
        "email": "testuser3@example.com",
        "password": "password3",
    }
    client.post("/users/create", json=data2)
    client.post("/users/create", json=data3)
    response = client.get("/users/show_all", headers=normal_user_token)
    assert response.status_code == 200
    all_users = response.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item


def test_show_myself(client: Any, normal_user_token: dict[str, str]) -> None:
    response = client.get("/users/show_user", headers=normal_user_token)
    assert response.status_code == 200
    assert response.json()["email"] == settings.TEST_USER_EMAIL
    assert response.json()["is_active"] == True
    assert response.json()["is_admin"] == False


def test_find_user_by_email(client: Any, normal_user_token: dict[str, str]) -> None:
    data4 = {
        "username": "testuser4",
        "email": "testuser4@example.com",
        "password": "password4",
    }
    client.post("/users/create", json=data4)
    response = client.get("/users/testuser4%40example.com", headers=normal_user_token)
    assert response.status_code == 200
    assert response.json()["email"] == "testuser4@example.com"


"""Tests for post routers."""


def test_create_post(client: Any, normal_user_token: dict[str, str]) -> None:
    data1 = {
        "title": "The test title",
        "content": "Some text by test",
        "date_creation": "2023-01-01T12:00:00.000Z",
    }

    response = client.post("/posts/create", json=data1, headers=normal_user_token)
    assert response.status_code == 200
    assert response.json()["title"] == data1["title"]
    assert response.json()["content"] == data1["content"]
    assert "user_id" in response.json()


def test_show_all(client: Any, normal_user_token: dict[str, str]) -> None:
    data2 = {
        "title": "The test2 title",
        "content": "Some text by test2",
        "date_creation": "2023-01-01T12:00:00.000Z",
    }

    data3 = {
        "title": "The test3 title",
        "content": "Some text by test3",
        "date_creation": "2023-01-01T12:00:00.000Z",
    }
    client.post("/posts/create", json=data2, headers=normal_user_token)
    client.post("/posts/create", json=data3, headers=normal_user_token)
    response = client.get("/posts/show_all", headers=normal_user_token)
    assert response.status_code == 200
    all_posts = response.json()
    assert len(all_posts) > 1
    for item in all_posts:
        assert "title" in item


def test_show_post(client: Any, normal_user_token: dict[str, str]) -> None:
    response = client.get("/posts/show/1", headers=normal_user_token)
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_update_post(client: Any, normal_user_token: dict[str, str]) -> None:
    data4 = {
        "title": "The test4 title",
        "content": "Some text by test4",
        "date_creation": "2023-01-01T12:00:00.000Z",
    }
    client.post("/posts/create", json=data4, headers=normal_user_token)
    data4["title"] = "The new test title"
    response = client.put("/posts/update/1", headers=normal_user_token, json=data4)
    assert response.status_code == 200
    assert response.json()["title"] == "The new test title"


def test_delete_post(client: Any, normal_user_token: dict[str, str]) -> None:
    data5 = {
        "title": "The test5 title",
        "content": "Some text by test5",
        "date_creation": "2023-01-01T12:00:00.000Z",
    }
    client.post("/posts/create", json=data5, headers=normal_user_token)
    client.delete("/posts/delete/1", headers=normal_user_token)
    response = client.get("/posts/show/1", headers=normal_user_token)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_like_post(client: Any, normal_user_token: dict[str, str]) -> None:
    data6 = {
        "title": "The test6 title",
        "content": "Some text by test6",
        "date_creation": "2023-01-01T12:00:00.000Z",
    }
    client.post("/posts/create", json=data6, headers=normal_user_token)
    response = client.post("/posts/like/2", headers=normal_user_token, json=data6)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_dislike_post(client: Any, normal_user_token: dict[str, str]) -> None:
    data7 = {
        "title": "The test7 title",
        "content": "Some text by test7",
        "date_creation": "2023-01-01T12:00:00.000Z",
    }
    client.post("/posts/create", json=data7, headers=normal_user_token)
    response = client.post("/posts/like/2", headers=normal_user_token, json=data7)
    assert response.status_code == status.HTTP_403_FORBIDDEN
