from app.config import Config

def test_login_success(client, test_user):
    login_data = {
        "username": test_user.email, # FastAPI OAuth2 utilise 'username' pour l'identifiant (email)
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