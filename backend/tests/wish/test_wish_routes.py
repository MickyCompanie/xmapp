from app.config import Config
from app.user.model import UserRole
from app.auth.utils import create_access_token
VALID_WISH_PAYLOAD = {
    "title": "Une superbe PS5 Pro",
    "description": "Pour jouer aux derniers jeux à Noël",
    "url": "https://example.com/ps5",
    "price_estimate": 799.99
}

# GET

def test_auth_user_get_wishes(auth_client, test_wish):
    response = auth_client.get(f"/{Config.PREFIX}{Config.VERSION}/wish/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["title"] == test_wish.title

def test_non_auth_user_dont_get_wishes(client):
    response = client.get(f"/{Config.PREFIX}{Config.VERSION}/wish/")
    assert response.status_code == 401

def test_auth_user_get_wish_by_id(auth_client, test_wish):
    response = auth_client.get(f"/{Config.PREFIX}{Config.VERSION}/wish/{test_wish.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_wish.id
    assert data["title"] == test_wish.title

def test_non_auth_user_dont_get_wish_by_id(client, test_wish):
    response = client.get(f"/{Config.PREFIX}{Config.VERSION}/wish/{test_wish.id}")
    assert response.status_code == 401

def test_get_wish_by_id_not_found(auth_client):
    invalid_id = 99999
    response = auth_client.get(f"/{Config.PREFIX}{Config.VERSION}/wish/{invalid_id}")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Wish not found"

# POST

def test_auth_user_can_create_wish(auth_client):
    """
        check that an auth user can create a wish and that the server return the wish with an id
    """

    response = auth_client.post(
        f'/{Config.PREFIX}{Config.VERSION}/wish/',
        json=VALID_WISH_PAYLOAD
    )

    assert response.status_code == 201

    data = response.json()
    assert data['title'] == VALID_WISH_PAYLOAD['title']
    assert data['price_estimate'] == VALID_WISH_PAYLOAD['price_estimate']
    assert 'id' in data
    assert isinstance(data['id'], int)


def test_non_auth_user_cant_create_wish(client):
    response = client.post(
        f'/{Config.PREFIX}{Config.VERSION}/wish/',
        json=VALID_WISH_PAYLOAD
    )
    assert response.status_code == 401
    assert 'detail' in response.json()

# PUT

def test_owner_can_update_their_own_wish(auth_client, test_user, wish_factory):
    mon_souhait = wish_factory(person_id=test_user.person_id, title="Console de jeux")
    
    payload = {
        "id": mon_souhait.id,
        "title": "PS5 Pro",
        "description": "Version 2To avec une deuxième manette"
    }
    
    response = auth_client.put(f"/{Config.PREFIX}{Config.VERSION}/wish/{mon_souhait.id}", json=payload)
    
    assert response.status_code == 200
    assert response.json()["title"] == "PS5 Pro"


def test_regular_user_cannot_update_other_users_wish(auth_client, user_factory, wish_factory):
    autre_user = user_factory(email="victime@example.com", role=UserRole.USER)
    souhait_victime = wish_factory(person_id=autre_user.person_id, title="Livre de cuisine")
    
    payload = {
        "id": souhait_victime.id,
        "title": "Hacked Title"
    }
    response = auth_client.put(f"/{Config.PREFIX}{Config.VERSION}/wish/{souhait_victime.id}", json=payload)
    
    assert response.status_code == 403


def test_admin_can_update_any_wish(client, user_factory, wish_factory):

    admin_user = user_factory(email="admin.wish@example.com", role=UserRole.ADMIN)
    un_user = user_factory(email="user.lambda@example.com", role=UserRole.USER)
    souhait_user = wish_factory(person_id=un_user.person_id, title="Vélo de course")
    
    token = create_access_token(data={"sub": admin_user.email})
    client.headers["Authorization"] = f"Bearer {token}"
    
    payload = {
        "id": souhait_user.id,
        "title": "Vélo électrique"
    }
    response = client.put(f"/{Config.PREFIX}{Config.VERSION}/wish/{souhait_user.id}", json=payload)
    
    assert response.status_code == 200
    assert response.json()["title"] == "Vélo électrique"


def test_santa_can_update_any_wish(santa_client, user_factory, wish_factory):
    un_user = user_factory(email="user.santa@example.com", role=UserRole.USER)
    souhait_user = wish_factory(person_id=un_user.person_id, title="Chocolats")
    
    payload = {
        "id": souhait_user.id,
        "title": "Chocolats Fins"
    }
    response = santa_client.put(f"/{Config.PREFIX}{Config.VERSION}/wish/{souhait_user.id}", json=payload)
    
    assert response.status_code == 200
    assert response.json()["title"] == "Chocolats Fins"


def test_update_wish_with_mismatched_id_should_fail(auth_client, test_user, wish_factory):
    mon_souhait = wish_factory(person_id=test_user.person_id, title="BD de collection")
    
    
    payload = {
        "id": 9999,
        "title": "Titre modifié"
    }
    response = auth_client.put(f"/{Config.PREFIX}{Config.VERSION}/wish/{mon_souhait.id}", json=payload)
    
    assert response.status_code == 400

def test_non_auth_user_cant_update_wish(client, test_wish):
    update_payload = {
        "id": test_wish.id,
        "title": "Tentative de piratage"
    }
    
    response = client.put(
        f"/{Config.PREFIX}{Config.VERSION}/wish/{test_wish.id}",
        json=update_payload
    )
    
    assert response.status_code == 401

# DELETE

def test_owner_can_delete_their_own_wish(auth_client, test_user, wish_factory, db_session):
    mon_souhait = wish_factory(person_id=test_user.person_id, title="Objet à supprimer")
    response = auth_client.delete(f"/{Config.PREFIX}{Config.VERSION}/wish/{mon_souhait.id}")
    assert response.status_code in [200, 204]


def test_regular_user_cannot_delete_other_users_wish(auth_client, user_factory, wish_factory):
    autre_user = user_factory(email="autre.owner@example.com", role=UserRole.USER)
    souhait_distant = wish_factory(person_id=autre_user.person_id, title="Trésor précieux")
    
    response = auth_client.delete(f"/{Config.PREFIX}{Config.VERSION}/wish/{souhait_distant.id}")
    
    assert response.status_code == 403


def test_admin_or_santa_can_delete_any_wish(santa_client, user_factory, wish_factory):
    un_user = user_factory(email="user.lambda2@example.com", role=UserRole.USER)
    souhait_user = wish_factory(person_id=un_user.person_id, title="Mauvaise idée de cadeau")
    
    response = santa_client.delete(f"/{Config.PREFIX}{Config.VERSION}/wish/{souhait_user.id}")
    
    assert response.status_code in [200, 204]


def test_delete_non_existent_wish_should_return_404(auth_client):
    response = auth_client.delete(f"/{Config.PREFIX}{Config.VERSION}/wish/99999")
    
    assert response.status_code == 404