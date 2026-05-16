from app.config import Config

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

def test_auth_user_can_update_wish(auth_client, test_wish):
    update_payload = {
        "id": test_wish.id,
        "title": "Une superbe PS5 Pro avec lecteur de disque" # Titre modifié
    }
    
    response = auth_client.put(
        f"/{Config.PREFIX}{Config.VERSION}/wish/{test_wish.id}", 
        json=update_payload
    )
    
    assert response.status_code == 200
    data = response.json()
    
    
    assert data["title"] == "Une superbe PS5 Pro avec lecteur de disque"
    assert data["description"] == test_wish.description

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

def test_update_wish_id_mismatch(auth_client, test_wish):
    wrong_id = test_wish.id + 1  
    
    update_payload = {
        "id": wrong_id, 
        "title": "Changement de titre incohérent"
    }
    
    response = auth_client.put(
        f"/{Config.PREFIX}{Config.VERSION}/wish/{test_wish.id}", 
        json=update_payload
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Bad id provided"

# DELETE

# TODO test_auth_user_can_delete_wish
# TODO test_non_auth_user_cant_delete_wish
# TODO test_delete_wish_not_found
