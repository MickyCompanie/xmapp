from app.config import Config


VALID_GIFT_PAYLOAD = {
    "title": "Une boîte de chocolats",
    "price_paid": 14.99,
    "url": "https://chocolat-online.com",
    "receiver_id": 2,
    "status": 'pending',
    }
    
# GET

#TODO only santa
def test_auth_user_can_get_all_gifts(auth_client, test_gift):
    response = auth_client.get(f"/{Config.PREFIX}{Config.VERSION}/gift/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    assert any(g["id"] == test_gift.id for g in data)

def test_non_auth_user_cannot_get_all_gifts(client):
    response = client.get(f"/{Config.PREFIX}{Config.VERSION}/gift/")
    assert response.status_code == 401

def test_auth_user_can_get_gift_by_id(auth_client, test_gift):
    response = auth_client.get(f"/{Config.PREFIX}{Config.VERSION}/gift/{test_gift.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_gift.id
    assert "title" in data
    assert "price_paid" in data

def test_non_auth_user_cannot_get_gift_by_id(client, test_gift):
    response = client.get(f"/{Config.PREFIX}{Config.VERSION}/gift/{test_gift.id}")
    assert response.status_code == 401

def test_get_gift_by_id_not_found(auth_client):
    invalid_id = 999999
    response = auth_client.get(f"/{Config.PREFIX}{Config.VERSION}/gift/{invalid_id}")
    
    assert response.status_code == 404

# POST

def test_auth_user_can_create_spontaneous_gift(auth_client, test_person_without_account):
    payload = {**VALID_GIFT_PAYLOAD, "receiver_id": test_person_without_account.id}
    
    response = auth_client.post(
        f"/{Config.PREFIX}{Config.VERSION}/gift/",
        json=payload
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["wish_id"] is None
    assert data["receiver_id"] == test_person_without_account.id


def test_auth_user_can_create_gift_from_wish(auth_client, test_wish, test_person_without_account):
    payload = {**VALID_GIFT_PAYLOAD, "receiver_id": test_person_without_account.id}
    
    response = auth_client.post(
        f"/{Config.PREFIX}{Config.VERSION}/gift/{test_wish.id}",
        json=payload
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["wish_id"] == test_wish.id
    assert data["receiver_id"] == test_person_without_account.id

def test_non_auth_user_cannot_create_gift(client, test_person_without_account):
    payload = {**VALID_GIFT_PAYLOAD, "receiver_id": test_person_without_account.id}
    
    response = client.post(
        f"/{Config.PREFIX}{Config.VERSION}/gift/", 
        json=payload
    )
    
    assert response.status_code == 401

# PUT

def test_auth_user_can_update_gift(auth_client, test_gift):
    payload = {
        "id": test_gift.id,
        "title": "PlayStation 5 Pro",  
        "price_paid": 549.99,          
        "status": "bought",         
        "receiver_id": test_gift.receiver_id
    }
    
    response = auth_client.put(
        f"/{Config.PREFIX}{Config.VERSION}/gift/{test_gift.id}",
        json=payload
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_gift.id
    assert data["title"] == "PlayStation 5 Pro"
    assert data["price_paid"] == 549.99
    assert data["status"] == "bought"

def test_non_auth_user_cannot_update_gift(client, test_gift):
    payload = {
        "title": "Tentative de piratage",
        "price_paid": 0.0,
        "status": "completed",
        "receiver_id": test_gift.receiver_id
    }
    
    response = client.put(
        f"/{Config.PREFIX}{Config.VERSION}/gift/{test_gift.id}",
        json=payload
    )
    
    assert response.status_code == 401

def test_update_gift_id_mismatch(auth_client, test_gift):
    invalid_id = 999999
    payload = {
        "id": test_gift.id,
        "title": "Changement de titre",
        "price_paid": 499.99,
        "status": "pending",
    }
    
    response = auth_client.put(
        f"/{Config.PREFIX}{Config.VERSION}/gift/{invalid_id}",
        json=payload
    )
    
    assert response.status_code in [400, 404]

# DELETE

def test_auth_user_can_delete_gift(auth_client, test_gift):
    """Un utilisateur connecté doit pouvoir supprimer son cadeau."""
    response = auth_client.delete(f"/{Config.PREFIX}{Config.VERSION}/gift/{test_gift.id}")
    assert response.status_code in [200, 204]
    
    get_response = auth_client.get(f"/{Config.PREFIX}{Config.VERSION}/gift/{test_gift.id}")
    assert get_response.status_code == 404


def test_non_auth_user_cannot_delete_gift(client, test_gift):
    response = client.delete(f"/{Config.PREFIX}{Config.VERSION}/gift/{test_gift.id}")
    assert response.status_code == 401