from app.config import Config
import jwt
from datetime import datetime, timedelta, timezone

def test_login_success(client, test_user):
    login_data = {
        "username": test_user.email, 
        "password": "password123"
    }
    
    response = client.post(f"/{Config.PREFIX}{Config.VERSION}/auth/login", data=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(client, test_user):
    login_data = {
        "username": test_user.email,
        "password": "wrongpassword"
    }
    
    response = client.post(f"/{Config.PREFIX}{Config.VERSION}/auth/login", data=login_data)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect Email or Password"

def test_login_user_not_found(client):
    login_data = {
        "username": "ghost@example.com",
        "password": "password123"
    }
    
    response = client.post(f"/{Config.PREFIX}{Config.VERSION}/auth/login", data=login_data)
    
    assert response.status_code == 401

def test_authenticated_route_access(auth_client):
    """Vérifie que le auth_client (qui a le token) peut accéder à une route protégée"""
    response = auth_client.get(f"/{Config.PREFIX}{Config.VERSION}/user/me")
    assert response.status_code == 200

def test_refresh_token_success(client, test_user):
    """Vérifie qu'un refresh token valide génère un nouvel access_token."""
    refresh_token = jwt.encode(
        {"sub": test_user.email},
        Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )

    response = client.post(
        f"/{Config.PREFIX}{Config.VERSION}/auth/refresh",
        json={"refresh_token": refresh_token}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token_invalid_format(client):
    """Vérifie le rejet d'un token malformé / invalide."""
    response = client.post(
        f"/{Config.PREFIX}{Config.VERSION}/auth/refresh",
        json={"refresh_token": "token_invalide_nimporte_quoi"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired refresh token"


def test_refresh_token_expired(client, test_user):
    """Vérifie le rejet d'un token dont la date d'expiration est dépassée."""
    expired_payload = {
        "sub": test_user.email,
        "exp": datetime.now(timezone.utc) - timedelta(minutes=10) 
    }
    expired_token = jwt.encode(
        expired_payload,
        Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )

    response = client.post(
        f"/{Config.PREFIX}{Config.VERSION}/auth/refresh",
        json={"refresh_token": expired_token}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired refresh token"


def test_refresh_token_missing_sub(client):
    """Vérifie le rejet d'un token JWT valide mais sans le champ 'sub' (email)."""
    payload_without_sub = {"role": "user"}
    token_without_sub = jwt.encode(
        payload_without_sub,
        Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )

    response = client.post(
        f"/{Config.PREFIX}{Config.VERSION}/auth/refresh",
        json={"refresh_token": token_without_sub}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired refresh token"


def test_refresh_token_user_not_found(client):
    """Vérifie le rejet si l'email encodé dans le token n'existe pas en BDD."""
    token = jwt.encode(
        {"sub": "ghost@example.com"},
        Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )

    response = client.post(
        f"/{Config.PREFIX}{Config.VERSION}/auth/refresh",
        json={"refresh_token": token}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired refresh token"


def test_refresh_token_inactive_user(client, user_factory, db_session):
    """Vérifie le rejet d'un refresh token si le compte de l'utilisateur est désactivé."""
    user = user_factory(email="inactive@example.com")
    user.is_active = False
    db_session.flush()

    token = jwt.encode(
        {"sub": user.email},
        Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )

    response = client.post(
        f"/{Config.PREFIX}{Config.VERSION}/auth/refresh",
        json={"refresh_token": token}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired refresh token"