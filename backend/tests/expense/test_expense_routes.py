import pytest
from fastapi import status
from app.config import Config
from app.expense.model import Expense, ExpenseStatus, ExpenseType
from app.repayment.model import Repayment, RepaymentStatus
from datetime import datetime, timezone



EXPENSE_URL = f"/{Config.PREFIX}{Config.VERSION}/expense/"


# GET

def test_get_all_expenses_success(db_session, user_factory, auth_client_factory):
    user = user_factory(email="buyer@example.com")
    
    expense_1 = Expense(
        title="Courses de Noël",
        total_amount=45.50,
        is_shared=False,
        payer_id=user.person_id,
        expense_type=ExpenseType.FOOD,
        status=ExpenseStatus.FULLY_REPAID
    )
    db_session.add(expense_1)
    db_session.commit()

    client = auth_client_factory(user)
    response = client.get(EXPENSE_URL)

    assert response.status_code == 200 #todo, passew par httpstatuscode ou equivalent fastapi'''
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["title"] == "Courses de Noël"


def test_get_expense_by_id_success(db_session, user_factory, auth_client_factory):
    user = user_factory(email="viewer@example.com")
    expense = Expense(
        title="Cadeau Commun",
        total_amount=100.00,
        is_shared=True,
        payer_id=user.person_id,
        expense_type=ExpenseType.OTHER,
        status=ExpenseStatus.PENDING  
    )
    db_session.add(expense)
    db_session.commit()
    db_session.refresh(expense)

    client = auth_client_factory(user)
    response = client.get(f"{EXPENSE_URL}{expense.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == expense.id
    assert data["title"] == "Cadeau Commun"
    assert float(data["total_amount"]) == 100.00


def test_get_expense_by_id_not_found(user_factory, auth_client_factory):
    user = user_factory(email="user@example.com")
    invalid_expense_id = 99999

    client = auth_client_factory(user)
    response = client.get(f"{EXPENSE_URL}{invalid_expense_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"



# POST

def test_create_expense_unauthenticated(client):
    expense_data = {
        "title": "Restau sans filet",
        "total_amount": 35.00,
        "expense_type": "FOOD",
        "is_shared": False
    }
    
    response = client.post(EXPENSE_URL, json=expense_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_expense_not_shared_success(user_factory, auth_client_factory, db_session):
    user = user_factory(email="solo@example.com")
    client = auth_client_factory(user)
    
    expense_data = {
        "title": "Abonnement internet",
        "total_amount": 29.99,
        "expense_type": "other",
        "status": "pending",
        "is_shared": False,
        "repayments": []
    }
    
    response = client.post(EXPENSE_URL, json=expense_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["title"] == "Abonnement internet"
    assert data["total_amount"] == 29.99
    assert data["is_shared"] is False
    
    db_expense = db_session.query(Expense).filter(Expense.id == data["id"]).first()
    assert db_expense is not None
    assert db_expense.payer_id == user.person_id


def test_create_expense_shared_with_repayments_success(user_factory, auth_client_factory, db_session):
    payer = user_factory(email="payer@example.com")
    debtor = user_factory(email="debtor@example.com")
    client = auth_client_factory(payer)

    db_session.flush() 
    db_session.refresh(debtor)


    expense_data = {
        "title": "Courses coloc",
        "total_amount": 60.00,
        "expense_type": "food",
        "status": "pending",
        "is_shared": True,
        "repayments": [
            {
                "debtor_id": debtor.person_id,
                "amount_to_pay": 30.00,
                "status": "pending"
            }
        ]
    }
    print("-----------------TEST---------------------")
    print(expense_data)
    response = client.post(EXPENSE_URL, json=expense_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert debtor.person_id is not None

    data = response.json()
    assert data["is_shared"] is True
    assert len(data["repayments"]) == 1
    assert data["repayments"][0]["debtor_id"] == debtor.person_id
    assert data["repayments"][0]["amount_to_pay"] == 30.00

    db_expense = db_session.query(Expense).filter(Expense.id == data["id"]).first()
    assert len(db_expense.repayments) == 1
    assert db_expense.repayments[0].amount_to_pay == 30.00
    assert db_expense.repayments[0].debtor_id == debtor.person_id

# Tests de Mise à jour (PUT)

def test_update_expense_wrong_id_mismatch(user_factory, auth_client_factory, db_session):
    payer = user_factory(email="payer_mismatch@example.com")
    client = auth_client_factory(payer)

    url_id = 1
    # ID dans le body (999) != ID dans l'URL (1)
    payload_mismatch = {
        "id": 999,
        "title": "Dépense Mismatch",
        "total_amount": 50.00,
        "expense_type": "food",
        "status": "pending",
        "is_shared": False,
        "repayments": []
    }

    url = f"{EXPENSE_URL.rstrip('/')}/{url_id}"
    response = client.put(url, json=payload_mismatch)

    assert response.status_code in (400, 422)
    detail_str = str(response.json().get("detail", "")).lower()
    assert "mismatch" in detail_str or "id" in detail_str


def test_update_expense_not_found(user_factory, auth_client_factory):
    payer = user_factory(email="payer_notfound@example.com")
    client = auth_client_factory(payer)

    non_existent_id = 99999
    update_payload = {
        "id": non_existent_id,  # Requis par ExpenseUpdate
        "title": "Inexistante",
        "total_amount": 30.00,
        "expense_type": "food",
        "status": "pending",
        "is_shared": False,
        "repayments": None
    }

    url = f"{EXPENSE_URL.rstrip('/')}/{non_existent_id}"
    response = client.put(url, json=update_payload)

    assert response.status_code == 404


def test_update_expense_fields_and_sync_repayments_success(user_factory, auth_client_factory, db_session):
    payer = user_factory(email="payer_sync@example.com")
    debtor1 = user_factory(email="debtor1@example.com")
    debtor2 = user_factory(email="debtor2@example.com")
    client = auth_client_factory(payer)

    db_session.flush()

    # 1. Création initiale
    initial_payload = {
        "title": "Soirée pizza",
        "total_amount": 40.00,
        "expense_type": "food",
        "status": "pending",
        "is_shared": True,
        "repayments": [
            {
                "debtor_id": debtor1.person_id,
                "amount_to_pay": 20.00,
                "status": "pending"
            }
        ]
    }
    create_resp = client.post(EXPENSE_URL, json=initial_payload)
    assert create_resp.status_code in (200, 201)
    expense_id = create_resp.json()["id"]

    # 2. Mise à jour avec status valide et champs RepaymentRead complets
    now_iso = datetime.now(timezone.utc).isoformat()
    update_payload = {
        "id": expense_id,
        "title": "Soirée pizza & boissons",
        "total_amount": 60.00,
        "expense_type": "food",
        "status": "fully_repaid",  # Valeurs valides: 'pending', 'partially_repaid', 'fully_repaid'
        "is_shared": True,
        "repayments": [
            {
                "id": 0,
                "expense_id": expense_id,
                "debtor_id": debtor2.person_id,
                "amount_to_pay": 30.00,
                "status": "pending",
                "created_at": now_iso,
                "updated_at": now_iso
            }
        ]
    }

    url = f"{EXPENSE_URL.rstrip('/')}/{expense_id}"
    response = client.put(url, json=update_payload)

    # 3. Assertions
    assert response.status_code == 200, f"Erreur de validation: {response.json()}"
    data = response.json()
    assert data["id"] == expense_id
    assert data["title"] == "Soirée pizza & boissons"
    assert data["status"] == "fully_repaid"


# Tests de Suppression (DELETE)


def test_delete_expense_success(user_factory, auth_client_factory, db_session):
    # 1. Préparation du client authentifié et création d'une dépense
    payer = user_factory(email="payer_delete@example.com")
    client = auth_client_factory(payer)

    initial_payload = {
        "title": "Dépense à supprimer",
        "total_amount": 25.00,
        "expense_type": "food",
        "status": "pending",
        "is_shared": False,
        "repayments": []
    }
    
    create_resp = client.post(EXPENSE_URL, json=initial_payload)
    assert create_resp.status_code in (200, 201)
    expense_id = create_resp.json()["id"]

    # 2. Exécution de la suppression
    url = f"{EXPENSE_URL.rstrip('/')}/{expense_id}"
    response = client.delete(url)

    # 3. Assertions
    # (Remplacez 200 par 204 si votre route renvoie status.HTTP_204_NO_CONTENT)
    assert response.status_code in (200, 204), f"Erreur lors de la suppression: {response.json() if response.content else ''}"

    # 4. Vérification que la dépense n'existe plus (recherche renvoie 404)
    get_resp = client.get(url)
    assert get_resp.status_code == 404


def test_delete_expense_not_found(user_factory, auth_client_factory):
    # 1. Préparation du client authentifié
    payer = user_factory(email="payer_delete_nf@example.com")
    client = auth_client_factory(payer)

    non_existent_id = 99999
    url = f"{EXPENSE_URL.rstrip('/')}/{non_existent_id}"

    # 2. Tentative de suppression d'un ID inexistant
    response = client.delete(url)

    # 3. Assertion
    assert response.status_code == 404