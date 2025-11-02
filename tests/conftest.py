import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import uuid

from app.main import app
from app.database import Base, get_db
from app.models.user import UserRole
from app.services.user_service import UserService

# Create in-memory SQLite database for testing
# Note: We use PostgreSQL in production, but SQLite for tests
# SQLite doesn't support UUID natively, so we store them as strings
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Enable foreign key constraints in SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def admin_user(db_session):
    """Create an admin user for testing."""
    user_service = UserService(db_session)
    return user_service.create_admin_user("admin@test.com", "admin123")


@pytest.fixture
def admin_token(client, admin_user):
    """Get admin authentication token."""
    response = client.post(
        "/auth/login",
        json={"email": "admin@test.com", "password": "admin123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def customer_user(db_session):
    """Create a customer user for testing."""
    user_service = UserService(db_session)
    from app.schemas.user import UserCreate
    user_data = UserCreate(
        email="customer@test.com",
        password="customer123",
        full_name="Test Customer",
        role=UserRole.CUSTOMER
    )
    return user_service.create_user(user_data)


@pytest.fixture
def customer_token(client, customer_user):
    """Get customer authentication token."""
    response = client.post(
        "/auth/login",
        json={"email": "customer@test.com", "password": "customer123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def restaurant_owner_user(db_session):
    """Create a restaurant owner user for testing."""
    user_service = UserService(db_session)
    from app.schemas.user import UserCreate
    user_data = UserCreate(
        email="owner@test.com",
        password="owner123",
        full_name="Test Owner",
        role=UserRole.RESTAURANT_OWNER
    )
    return user_service.create_user(user_data)


@pytest.fixture
def restaurant_owner_token(client, restaurant_owner_user):
    """Get restaurant owner authentication token."""
    response = client.post(
        "/auth/login",
        json={"email": "owner@test.com", "password": "owner123"}
    )
    return response.json()["access_token"]

