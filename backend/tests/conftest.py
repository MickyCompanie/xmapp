import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app import app
from app.db import Base, get_db
from app.config import Config
from app.auth.utils import create_access_token

from app.user.model import UserRole
from app.wish.model import Wish
from app.person.model import Person
from app.gift.model import Gift
from app.expense.model import Expense, ExpenseStatus, ExpenseType
from app.repayment.model import Repayment, RepaymentStatus

engine = create_engine(
    Config.TEST_DATABASE_URL,
    connect_args={"options": "-c client_encoding=utf8"} # force l'utf8 pour return français de postgres
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def user_factory(db_session):
    from app.user.model import User, UserRole
    from app.person.model import Person
    from app.auth.utils import hash_password

    def _create_user(email: str, role: UserRole = UserRole.USER):
        person = Person(
            first_name=f"Prenom_{role.value.lower()}", 
            last_name="Nom_Test"
        )
        db_session.add(person)
        db_session.flush() 
        
        user = User(
            email=email,
            hashed_password=hash_password("password123"),
            is_active=True,
            role=role,
            person=person
        )
        db_session.add(user)
        db_session.flush()
        db_session.refresh(user)
        return user
        
    return _create_user

@pytest.fixture
def auth_client_factory(db_session):
    from fastapi.testclient import TestClient

    def _generate_client(user):
        local_client = TestClient(app)
        
        def override_get_db():
            try:
                yield db_session
            finally:
                pass
        app.dependency_overrides[get_db] = override_get_db
        
        access_token = create_access_token(data={"sub": user.email})
        local_client.headers["Authorization"] = f"Bearer {access_token}"
        
        return local_client
        
    return _generate_client

@pytest.fixture
def test_user(user_factory):
    from app.user.model import UserRole
    return user_factory(email="test@example.com", role=UserRole.USER)

@pytest.fixture
def auth_client(client, test_user):
    access_token = create_access_token(data={"sub": test_user.email})
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}"
    }
    return client

@pytest.fixture
def test_santa_user(user_factory):
    from app.user.model import UserRole
    return user_factory(email="santa@example.com", role=UserRole.SANTA)


@pytest.fixture
def santa_client(client, test_santa_user):
    access_token = create_access_token(data={"sub": test_santa_user.email})
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}"
    }
    return client

@pytest.fixture
def wish_factory(db_session):
    """Factory pour créer des souhaits (Wish) à la volée dans les tests."""
    from app.wish.model import Wish

    def _create_wish(person_id: int, title: str = "Cadeau Surprise", description: str = "Une description"):
        wish = Wish(
            title=title,
            description=description,
            url="https://example.com/item",
            price_estimate=29.99,
            person_id=person_id
        )
        db_session.add(wish)
        db_session.flush()
        db_session.refresh(wish)
        return wish

    return _create_wish


@pytest.fixture
def test_wish(wish_factory, test_user):
    return wish_factory(
        person_id=test_user.person_id,
        title="Console de jeux",
        description="Version Standard avec deux manettes"
    )

@pytest.fixture
def test_person_without_account(db_session):
    person = Person(
        first_name="Jean",
        last_name="Dupont"
    )
    db_session.add(person)
    db_session.flush()
    db_session.refresh(person)
    return person

@pytest.fixture
def test_gift(db_session, test_user, test_person_without_account):
    gift = Gift(
        title="PlayStation 5",
        price_paid=499.99,
        giver_id=test_user.person.id,
        receiver_id=test_person_without_account.id
    )
    db_session.add(gift)
    db_session.flush()
    db_session.refresh(gift)
    return gift

@pytest.fixture
def test_expense(db_session, test_user):
    """Crée une dépense de test rattachée à l'utilisateur connecté."""
    expense = Expense(
        title="Dépense de test",
        total_amount=50.0,
        is_shared=True,
        payer_id=test_user.person_id,
        expense_type=ExpenseType.FOOD,
        status=ExpenseStatus.PENDING
    )
    db_session.add(expense)
    db_session.flush()
    db_session.refresh(expense)
    return expense

@pytest.fixture
def test_repayment(db_session, test_expense, test_person_without_account):
    """Crée un remboursement de test."""
    repayment = Repayment(
        expense_id=test_expense.id,
        debtor_id=test_person_without_account.id,
        amount_to_pay=25.0,
        status=RepaymentStatus.PENDING
    )
    db_session.add(repayment)
    db_session.flush()
    db_session.refresh(repayment)
    return repayment