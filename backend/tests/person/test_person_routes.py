from app.config import Config

VALID_PERSON_PAYLOAD = {
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "1995-12-25T00:00:00"
}

# GET

def test_auth_user_can_get_all_person(auth_client, test_person_without_account):
    response = auth_client.get(f"/{Config.PREFIX}{Config.VERSION}/person/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) >= 1
    
    person_titles = [p["first_name"] for p in data]
    assert test_person_without_account.first_name in person_titles

def test_non_auth_user_cannot_get_all_person(client):
    response = client.get(f"/{Config.PREFIX}{Config.VERSION}/person/")
    assert response.status_code == 401

def test_auth_user_can_get_a_person_by_id(auth_client, test_person_without_account):
    response = auth_client.get(
        f"/{Config.PREFIX}{Config.VERSION}/person/{test_person_without_account.id}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_person_without_account.id
    assert data["first_name"] == test_person_without_account.first_name

def test_non_auth_user_cannot_get_a_person_by_id(client, test_person_without_account):
    response = client.get(
        f"/{Config.PREFIX}{Config.VERSION}/person/{test_person_without_account.id}"
    )
    assert response.status_code == 401

def test_get_person_by_id_not_found(auth_client):
    invalid_id = 99999
    response = auth_client.get(f"/{Config.PREFIX}{Config.VERSION}/person/{invalid_id}")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Person not found"

# POST

def test_auth_user_can_create_person(auth_client):
    response = auth_client.post(
        f"/{Config.PREFIX}{Config.VERSION}/person/", 
        json=VALID_PERSON_PAYLOAD
    )
    
    assert response.status_code == 201
    
    data = response.json()
    assert data["first_name"] == VALID_PERSON_PAYLOAD["first_name"]
    assert data["last_name"] == VALID_PERSON_PAYLOAD["last_name"]
    assert "id" in data
    assert isinstance(data["id"], int)

def test_non_auth_user_cannot_create_person(client):
    response = client.post(
        f"/{Config.PREFIX}{Config.VERSION}/person/", 
        json=VALID_PERSON_PAYLOAD
    )
    
    assert response.status_code == 401
    assert "detail" in response.json()

# PUT

def test_auth_user_can_update_person(auth_client, test_person_without_account):
    update_payload = {
        "id": test_person_without_account.id,
        "first_name": "NouveauPrénom" 
    }
    
    response = auth_client.put(
        f"/{Config.PREFIX}{Config.VERSION}/person/{test_person_without_account.id}", 
        json=update_payload
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["first_name"] == "NouveauPrénom"
    assert data["last_name"] == test_person_without_account.last_name

def test_non_auth_user_cannot_update_person(client, test_person_without_account):
    update_payload = {
        "id": test_person_without_account.id,
        "first_name": "Pirate"
    }
    
    response = client.put(
        f"/{Config.PREFIX}{Config.VERSION}/person/{test_person_without_account.id}", 
        json=update_payload
    )
    assert response.status_code == 401

def test_update_person_id_mismatch(auth_client, test_person_without_account):
    wrong_id = test_person_without_account.id + 1
    
    update_payload = {
        "id": wrong_id,
        "first_name": "Incohérent"
    }
    
    response = auth_client.put(
        f"/{Config.PREFIX}{Config.VERSION}/person/{test_person_without_account.id}", 
        json=update_payload
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Bad id provided"

# DELETE

def test_auth_user_can_delete_person(auth_client, test_person_without_account):
    response = auth_client.delete(
        f"/{Config.PREFIX}{Config.VERSION}/person/{test_person_without_account.id}"
    )
    
    assert response.status_code == 200

def test_non_auth_user_cannot_delete_person(client, test_person_without_account):
    response = client.delete(
        f"/{Config.PREFIX}{Config.VERSION}/person/{test_person_without_account.id}"
    )
    assert response.status_code == 401

def test_cannot_delete_person_with_user_account(auth_client, test_user):
    person_id_with_account = test_user.person_id 
    
    response = auth_client.delete(
        f"/{Config.PREFIX}{Config.VERSION}/person/{person_id_with_account}"
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot delete a person with a user account"