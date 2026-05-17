import pytest
from app.config import Config
from app.user.model import UserRole
from app.auth.utils import create_access_token

def test_get_all_users_as_admin_should_succeed(client, user_factory):
    admin_user = user_factory(email="admin.test@example.com", role=UserRole.ADMIN)
    
    token = create_access_token(data={"sub": admin_user.email})
    client.headers["Authorization"] = f"Bearer {token}"
    
    response = client.get(f"/{Config.PREFIX}{Config.VERSION}/user/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_all_users_as_santa_should_succeed(santa_client):
    response = santa_client.get(f"/{Config.PREFIX}{Config.VERSION}/user/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_all_users_as_regular_user_should_fail(auth_client):
    response = auth_client.get(f"/{Config.PREFIX}{Config.VERSION}/user/")
    assert response.status_code == 403

def test_get_all_users_unauthenticated_should_fail(client):
    response = client.get(f"/{Config.PREFIX}{Config.VERSION}/user/")
    assert response.status_code == 401


def test_get_other_user_profile_as_regular_user_should_fail(auth_client, user_factory):
    autre_user = user_factory(email="autre.user@example.com", role=UserRole.USER)
    
    response = auth_client.get(f"/{Config.PREFIX}{Config.VERSION}/user/{autre_user.id}")
    
    assert response.status_code == 403


def test_get_other_user_profile_as_admin_should_succeed(client, user_factory):
    admin_user = user_factory(email="super.admin@example.com", role=UserRole.ADMIN)
    test_user = user_factory(email="cible@example.com", role=UserRole.USER)
    
    token = create_access_token(data={"sub": admin_user.email})
    client.headers["Authorization"] = f"Bearer {token}"
    
    response = client.get(f"/{Config.PREFIX}{Config.VERSION}/user/{test_user.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id


def test_inactive_user_cannot_login(client, user_factory, db_session):
    """Un utilisateur désactivé ne doit pas pouvoir se connecter (400 ou 401)."""
    # 1. On crée le user via la factory
    inactive_user = user_factory(email="ban@example.com", role=UserRole.USER)
    
    # 2. On le force à False et on ENREGISTRE en BDD
    inactive_user.is_active = False
    db_session.add(inactive_user)
    db_session.commit()
    
    # 3. TENTATIVE DE LOGIN
    login_payload = {
        "username": inactive_user.email,
        "password": "password123"
    }
    response = client.post(f"/{Config.PREFIX}{Config.VERSION}/auth/login", data=login_payload)
    
    # On s'attend à un refus
    assert response.status_code in [400, 401]


def test_inactive_user_with_valid_token_is_blocked_on_routes(client, user_factory):
    inactive_user = user_factory(email="banned.token@example.com", role=UserRole.USER)
    inactive_user.is_active = False
    
    token = create_access_token(data={"sub": inactive_user.email})
    client.headers["Authorization"] = f"Bearer {token}"
    
    response = client.get(f"/{Config.PREFIX}{Config.VERSION}/user/{inactive_user.id}")
    
    assert response.status_code in [401, 403]

def test_update_user_as_admin_should_succeed(client, user_factory):
    admin_user = user_factory(email="admin.updater@example.com", role=UserRole.ADMIN)
    cible_user = user_factory(email="to.update@example.com", role=UserRole.USER)
    
    token = create_access_token(data={"sub": admin_user.email})
    client.headers["Authorization"] = f"Bearer {token}"
    
    payload = {
        "id": cible_user.id,
        "email": "updated.email@example.com"
    }
    response = client.put(f"/{Config.PREFIX}{Config.VERSION}/user/{cible_user.id}", json=payload)
    
    assert response.status_code == 200
    assert response.json()["email"] == "updated.email@example.com"


def test_update_user_as_regular_user_should_fail(auth_client, user_factory):
    cible_user = user_factory(email="protected@example.com", role=UserRole.USER)
    
    payload = {"email": "hacked@example.com"}
    response = auth_client.put(f"/{Config.PREFIX}{Config.VERSION}/user/{cible_user.id}", json=payload)
    
    assert response.status_code == 403

def test_reactivate_user_as_santa_should_succeed(santa_client, user_factory):
    test_user = user_factory(email="inactive@example.com", role=UserRole.USER)

    payload = {
        "id": test_user.id
    }
    response = santa_client.post(f"/{Config.PREFIX}{Config.VERSION}/user/reactivate/{test_user.id}", json=payload)
    
    assert response.status_code == 200
    assert response.json()["id"] == test_user.id


def test_reactivate_user_as_regular_user_should_fail(auth_client, user_factory):
    test_user = user_factory(email="stay.inactive@example.com", role=UserRole.USER)
    
    payload = {"is_active": True}
    response = auth_client.post(f"/{Config.PREFIX}{Config.VERSION}/user/reactivate/{test_user.id}", json=payload)
    
    assert response.status_code == 403