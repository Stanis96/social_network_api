from typing import Any


def test_create_user(client: Any):
    data = {
        "username": "someuser",
        "email": "someuser@example.com",
        "password": "password1",
    }
    response = client.post("/users/create", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == "someuser@example.com"
    assert response.json()["is_active"] == True
    assert response.json()["is_admin"] == False
