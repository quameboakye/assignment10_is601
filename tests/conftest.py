import pytest
from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal, engine
from app.models.user import User
from app.database_init import Base

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create database tables before session and drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """Provide a fresh database session with nested transaction support for tests."""
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection, join_transaction_mode="create_savepoint")
    
    
    yield session
    
    session.close()
    try:
        transaction.rollback()
    except Exception:
        pass
    connection.close()

@pytest.fixture
def managed_db_session(db_session):
    """Fixture providing a managed database session for tests."""
    return db_session

def create_fake_user(username=None, email=None, password="password123"):
    """Helper function returning a dictionary of user data, matching test unpacking expectations."""
    uid = uuid4().hex[:8]
    return {
        "first_name": "Test",
        "last_name": "User",
        "username": username or f"user_{uid}",
        "email": email or f"user_{uid}@example.com",
        "password": password,
    }

@pytest.fixture
def test_user(db_session):
    """Fixture to create, commit, and return a persisted test user object."""
    uid = uuid4().hex[:8]
    user_data = create_fake_user(username=f"test_{uid}", email=f"test_{uid}@example.com")
    hashed_pw = User.hash_password(user_data["password"]) if hasattr(User, "hash_password") else user_data["password"]
    
    user_kwargs = {
        "username": user_data["username"],
        "email": user_data["email"],
        "first_name": user_data["first_name"],
        "last_name": user_data["last_name"],
        "is_active": True,
        "is_verified": True
    }
    if hasattr(User, "hashed_password"):
        user_kwargs["hashed_password"] = hashed_pw
    else:
        user_kwargs["password"] = hashed_pw

    user = User(**user_kwargs)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def seed_users(db_session):
    """Fixture to seed multiple users for query testing."""
    users = []
    for i in range(3):
        uid = uuid4().hex[:8]
        user_data = create_fake_user(username=f"seed_{i}_{uid}", email=f"seed_{i}_{uid}@example.com")
        hashed_pw = User.hash_password(user_data["password"]) if hasattr(User, "hash_password") else user_data["password"]
        
        user_kwargs = {
            "username": user_data["username"],
            "email": user_data["email"],
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "is_active": True,
            "is_verified": True
        }
        if hasattr(User, "hashed_password"):
            user_kwargs["hashed_password"] = hashed_pw
        else:
            user_kwargs["password"] = hashed_pw

        user = User(**user_kwargs)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        users.append(user)
    return users

@pytest.fixture
def fake_user_data():
    """Fixture providing dictionary data for user registration tests."""
    uid = uuid4().hex[:8]
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": f"john.doe_{uid}@example.com",
        "username": f"johndoe_{uid}",
        "password": "SecurePassword123"
    }