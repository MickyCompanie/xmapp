from app.config import Config
from app.wish.model import Wish


VALID_GIFT_PAYLOAD = {
    "title": "Une boîte de chocolats",
    "price_paid": 14.99,
    "url": "https://chocolat-online.com",
    "receiver_id": 2,
    "status": "pending",
}

# GET

def test_santa_user_can_get_all_gifts(santa_client, test_gift):
    """Un utilisateur SANTA doit pouvoir récupérer la liste complète des cadeaux."""
    response = santa_client.get(f"/{Config.PREFIX}{Config.VERSION}/gift/")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    gifts = data.get("gifts", [])
    assert any(g["id"] == test_gift.id for g in gifts)


def test_regular_auth_user_only_sees_their_owned_gifts(
    auth_client, test_gift, db_session
):
    """Un utilisateur classique ne doit voir que les cadeaux qu'il offre."""
    from app.gift.model import Gift
    from app.person.model import Person

    person_giver = Person(first_name="Intrus", last_name="Giver")
    person_receiver = Person(first_name="Intrus", last_name="Receiver")
    db_session.add_all([person_giver, person_receiver])
    db_session.flush()

    intrus_gift = Gift(
        title="Cadeau Secret",
        giver_id=person_giver.id,
        receiver_id=person_receiver.id,
    )
    db_session.add(intrus_gift)
    db_session.commit()

    response = auth_client.get(f"/{Config.PREFIX}{Config.VERSION}/gift/")
    assert response.status_code == 200
    data = response.json()

    gifts = data.get("gifts", [])
    assert any(g["id"] == test_gift.id for g in gifts)
    assert not any(g["id"] == intrus_gift.id for g in gifts)


def test_non_auth_user_cannot_get_all_gifts(client):
    response = client.get(f"/{Config.PREFIX}{Config.VERSION}/gift/")
    assert response.status_code == 401


def test_auth_user_can_get_gift_by_id(auth_client, test_gift):
    response = auth_client.get(
        f"/{Config.PREFIX}{Config.VERSION}/gift/{test_gift.id}"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_gift.id
    assert "title" in data
    assert "price_paid" in data


def test_non_auth_user_cannot_get_gift_by_id(client, test_gift):
    response = client.get(
        f"/{Config.PREFIX}{Config.VERSION}/gift/{test_gift.id}"
    )
    assert response.status_code == 401


def test_get_gift_by_id_not_found(auth_client):
    invalid_id = 999999
    response = auth_client.get(
        f"/{Config.PREFIX}{Config.VERSION}/gift/{invalid_id}"
    )

    assert response.status_code == 404

# POST

def test_auth_user_can_create_spontaneous_gift(
    auth_client, test_person_without_account
):
    """Création d'un cadeau spontané (sans souhait associé) avec un payload JSON."""
    payload = {
        **VALID_GIFT_PAYLOAD,
        "receiver_id": test_person_without_account.id,
    }

    response = auth_client.post(
        f"/{Config.PREFIX}{Config.VERSION}/gift/", json=payload
    )

    assert response.status_code == 201
    data = response.json()
    assert data["wish_id"] is None
    assert data["receiver_id"] == test_person_without_account.id


def test_auth_user_can_create_gift_from_wish(
    auth_client, test_person_without_account, db_session
):
    """Création d'un cadeau à partir du souhait d'une AUTRE personne."""
    other_wish = Wish(
        title="Console de jeux",
        price_estimate=29.99,
        person_id=test_person_without_account.id,
    )
    db_session.add(other_wish)
    db_session.commit()

    response = auth_client.post(
        f"/{Config.PREFIX}{Config.VERSION}/gift/{other_wish.id}"
    )

    assert response.status_code == 201
    data = response.json()
    assert data["wish_id"] == other_wish.id
    assert data["title"] == other_wish.title
    assert data["price_paid"] == other_wish.price_estimate
    assert data["receiver_id"] == test_person_without_account.id


def test_user_cannot_create_gift_from_own_wish(
    auth_client, test_user, db_session
):
    """Un utilisateur ne doit pas pouvoir créer un cadeau depuis son propre souhait."""
    own_wish = Wish(
        title="Mon propre souhait",
        price_estimate=20.0,
        person_id=test_user.person_id,
    )
    db_session.add(own_wish)
    db_session.commit()

    response = auth_client.post(
        f"/{Config.PREFIX}{Config.VERSION}/gift/{own_wish.id}"
    )

    assert response.status_code == 400
    assert "propre liste" in response.json().get("detail", "")


def test_create_gift_from_wish_not_found(auth_client):
    """Tentative de création de cadeau depuis un souhait inexistant."""
    invalid_wish_id = 999999
    response = auth_client.post(
        f"/{Config.PREFIX}{Config.VERSION}/gift/{invalid_wish_id}"
    )

    assert response.status_code == 404


def test_non_auth_user_cannot_create_gift(client, test_person_without_account):
    """Un utilisateur anonyme ne peut pas créer un cadeau spontané."""
    payload = {
        **VALID_GIFT_PAYLOAD,
        "receiver_id": test_person_without_account.id,
    }

    response = client.post(
        f"/{Config.PREFIX}{Config.VERSION}/gift/", json=payload
    )

    assert response.status_code == 401


def test_non_auth_user_cannot_create_gift_from_wish(client, test_wish):
    """Un utilisateur anonyme ne peut pas créer un cadeau depuis un souhait."""
    response = client.post(
        f"/{Config.PREFIX}{Config.VERSION}/gift/{test_wish.id}"
    )

    assert response.status_code == 401

# PUT

def test_auth_user_can_update_gift(auth_client, test_gift):
    payload = {
        "id": test_gift.id,
        "title": "PlayStation 5 Pro",
        "price_paid": 549.99,
        "status": "bought",
        "receiver_id": test_gift.receiver_id,
    }

    response = auth_client.put(
        f"/{Config.PREFIX}{Config.VERSION}/gift/{test_gift.id}", json=payload
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
        "receiver_id": test_gift.receiver_id,
    }

    response = client.put(
        f"/{Config.PREFIX}{Config.VERSION}/gift/{test_gift.id}", json=payload
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
        f"/{Config.PREFIX}{Config.VERSION}/gift/{invalid_id}", json=payload
    )

    assert response.status_code in [400, 404]

# DELETE

def test_auth_user_can_delete_gift(auth_client, test_gift):
    """Un utilisateur connecté doit pouvoir supprimer son cadeau."""
    response = auth_client.delete(
        f"/{Config.PREFIX}{Config.VERSION}/gift/{test_gift.id}"
    )
    assert response.status_code in [200, 204]

    get_response = auth_client.get(
        f"/{Config.PREFIX}{Config.VERSION}/gift/{test_gift.id}"
    )
    assert get_response.status_code == 404


def test_non_auth_user_cannot_delete_gift(client, test_gift):
    response = client.delete(
        f"/{Config.PREFIX}{Config.VERSION}/gift/{test_gift.id}"
    )
    assert response.status_code == 401