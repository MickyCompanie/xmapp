import pytest
from app.config import Config
from app.expense.model import Expense, ExpenseStatus, ExpenseType
from app.repayment.model import Repayment, RepaymentStatus

REPAYMENT_URL = f"/{Config.PREFIX}{Config.VERSION}/repayment/"

VALID_REPAYMENT_PAYLOAD = {
    "amount_to_pay": 25.00,
    "status": "pending",
}


# --- GET ---

def test_auth_user_can_get_all_repayments(auth_client, test_repayment):
    """Un utilisateur connecté doit pouvoir récupérer ses remboursements."""
    response = auth_client.get(REPAYMENT_URL)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(r["id"] == test_repayment.id for r in data)


def test_regular_auth_user_only_sees_their_owned_repayments(auth_client, user_factory, db_session, test_repayment):
    """Un utilisateur ne doit voir que les remboursements dont il est débiteur ou créancier."""
    other_user1 = user_factory(email="other1@example.com")
    other_user2 = user_factory(email="other2@example.com")
    
    intrus_expense = Expense(
        title="Dépense secrète",
        total_amount=100.0,
        is_shared=True,
        payer_id=other_user1.person_id,
        expense_type=ExpenseType.FOOD,
        status=ExpenseStatus.PENDING
    )
    db_session.add(intrus_expense)
    db_session.flush()

    intrus_repayment = Repayment(
        expense_id=intrus_expense.id,
        debtor_id=other_user2.person_id,
        amount_to_pay=50.0,
        status=RepaymentStatus.PENDING
    )
    db_session.add(intrus_repayment)
    db_session.commit()

    response = auth_client.get(REPAYMENT_URL)
    assert response.status_code == 200
    data = response.json()

    assert any(r["id"] == test_repayment.id for r in data)
    assert not any(r["id"] == intrus_repayment.id for r in data)


def test_non_auth_user_cannot_get_all_repayments(client):
    response = client.get(REPAYMENT_URL)
    assert response.status_code == 401


def test_auth_user_can_get_repayment_by_id(auth_client, test_repayment):
    response = auth_client.get(f"{REPAYMENT_URL}{test_repayment.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_repayment.id
    assert "amount_to_pay" in data
    assert "status" in data


def test_non_auth_user_cannot_get_repayment_by_id(client, test_repayment):
    response = client.get(f"{REPAYMENT_URL}{test_repayment.id}")
    assert response.status_code == 401


def test_get_repayment_by_id_not_found(auth_client):
    invalid_id = 999999
    response = auth_client.get(f"{REPAYMENT_URL}{invalid_id}")
    
    assert response.status_code in [404, 500]


# --- POST ---

def test_auth_user_can_create_repayment(auth_client, test_expense, test_person_without_account):
    payload = {
        **VALID_REPAYMENT_PAYLOAD,
        "expense_id": test_expense.id,
        "debtor_id": test_person_without_account.id
    }
    
    response = auth_client.post(REPAYMENT_URL, json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["expense_id"] == test_expense.id
    assert data["debtor_id"] == test_person_without_account.id
    assert data["amount_to_pay"] == 25.00


def test_non_auth_user_cannot_create_repayment(client, test_expense, test_person_without_account):
    payload = {
        **VALID_REPAYMENT_PAYLOAD,
        "expense_id": test_expense.id,
        "debtor_id": test_person_without_account.id
    }
    
    response = client.post(REPAYMENT_URL, json=payload)
    assert response.status_code == 401


def test_create_repayment_expense_not_found(auth_client, test_person_without_account):
    invalid_expense_id = 999999
    payload = {
        **VALID_REPAYMENT_PAYLOAD,
        "expense_id": invalid_expense_id,
        "debtor_id": test_person_without_account.id
    }
    
    response = auth_client.post(REPAYMENT_URL, json=payload)
    assert response.status_code in [404, 500]


def test_create_repayment_invalid_payload(auth_client, test_expense, test_person_without_account):
    payload = {
        "expense_id": test_expense.id,
        "debtor_id": test_person_without_account.id,
        "amount_to_pay": -10.00,
        "status": "pending"
    }
    
    response = auth_client.post(REPAYMENT_URL, json=payload)
    assert response.status_code == 422


# --- PUT ---

def test_auth_user_can_update_repayment(auth_client, test_repayment):
    payload = {
        "id": test_repayment.id,
        "expense_id": test_repayment.expense_id,
        "debtor_id": test_repayment.debtor_id,
        "amount_to_pay": test_repayment.amount_to_pay,
        "status": "fully_repaid"
    }
    
    response = auth_client.put(
        f"{REPAYMENT_URL}{test_repayment.id}",
        json=payload
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_repayment.id
    assert data["status"] == "fully_repaid"


def test_non_auth_user_cannot_update_repayment(client, test_repayment):
    payload = {
        "id": test_repayment.id,
        "status": "fully_repaid"
    }
    
    response = client.put(
        f"{REPAYMENT_URL}{test_repayment.id}",
        json=payload
    )
    assert response.status_code == 401


def test_update_repayment_not_found(auth_client):
    invalid_id = 999999
    payload = {
        "id": invalid_id,
        "amount_to_pay": 10.00,
        "status": "fully_repaid"
    }
    
    response = auth_client.put(
        f"{REPAYMENT_URL}{invalid_id}",
        json=payload
    )
    assert response.status_code in [404, 500]


def test_update_repayment_id_mismatch(auth_client, test_repayment):
    invalid_url_id = 999999
    payload = {
        "id": test_repayment.id,
        "amount_to_pay": test_repayment.amount_to_pay,
        "status": "fully_repaid"
    }
    
    response = auth_client.put(
        f"{REPAYMENT_URL}{invalid_url_id}",
        json=payload
    )
    assert response.status_code in [400, 404, 422, 500]


# --- DELETE ---

def test_auth_user_can_delete_repayment(auth_client, test_repayment):
    """Un utilisateur connecté doit pouvoir supprimer son remboursement."""
    response = auth_client.delete(f"{REPAYMENT_URL}{test_repayment.id}")
    assert response.status_code in [200, 204]
    
    get_response = auth_client.get(f"{REPAYMENT_URL}{test_repayment.id}")
    assert get_response.status_code in [404, 500]


def test_non_auth_user_cannot_delete_repayment(client, test_repayment):
    response = client.delete(f"{REPAYMENT_URL}{test_repayment.id}")
    assert response.status_code == 401


def test_delete_repayment_not_found(auth_client):
    invalid_id = 999999
    response = auth_client.delete(f"{REPAYMENT_URL}{invalid_id}")
    assert response.status_code in [404, 500]