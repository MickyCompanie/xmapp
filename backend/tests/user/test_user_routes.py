from app.config import Config

def test_create_user(client):
    response = client.post(
        f"/{Config.PREFIX}{Config.VERSION}/user/signup",
        json={"email": "tester@example.com", "password": "password123", "first_name": "tester", "last_name": "testing"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "tester@example.com"

def test_get_me_unauthorized(client):
    response = client.get(f"/{Config.PREFIX}{Config.VERSION}/user/me")
    assert response.status_code == 401

def test_get_all_active_users(auth_client):
    response = auth_client.get(f"/{Config.PREFIX}{Config.VERSION}/user/")
    assert response.status_code == 200


def test_get_me_success(auth_client, test_user):
    response = auth_client.get(f"/{Config.PREFIX}{Config.VERSION}/user/me")
    assert response.status_code == 200
    assert response.json()["email"] == test_user.email