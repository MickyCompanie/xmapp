import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app import app
from app.db import Base, get_db
from app.config import Config
from app.auth.utils import create_access_token

from app.wish.model import Wish

engine = create_engine(
    Config.TEST_DATABASE_URL,
    connect_args={"options": "-c client_encoding=utf8"} # <--- force l'utf8 pour return français de postgres
    )
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Crée les tables au début de la session et les supprime à la fin."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """Donne une session DB propre pour chaque test avec un rollback automatique."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    """Override la dépendance get_db pour utiliser la DB de test."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # On nettoie l'override après le test
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_session):
    from app.user.model import User
    from app.person.model import Person
    from app.auth.utils import hash_password

    
    person = Person(first_name="Test", last_name="User")
    db_session.add(person)
    db_session.flush()
    
    user = User(
        email="test@example.com",
        hashed_password=hash_password("password123"),
        is_active=True,
        person=person
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def auth_client(client, test_user):
    """Renvoie un TestClient avec le header Authorization déjà rempli."""
    access_token = create_access_token(data={"sub": test_user.email})
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}"
    }
    return client

@pytest.fixture
def test_wish(db_session, test_user):
    """Crée un souhait lié à notre utilisateur de test"""
    wish = Wish(
        title="Console de jeux",
        description="Version Standard avec deux manettes",
        url="https://example.com/console",
        price_estimate=499.99,
        person_id=test_user.person_id 
    )
    db_session.add(wish)
    db_session.commit()
    db_session.refresh(wish)
    return wish