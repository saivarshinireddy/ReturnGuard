
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import create_app
from app.db.base import Base
from app.db.database import get_db
import app.models


@pytest.fixture
def client():
    # Create an isolated in-memory SQLite database
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )

    # Create tables in the test database
    Base.metadata.create_all(bind=test_engine)

    # Override the application's database dependency
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    test_app = create_app(testing=True)
    test_app.dependency_overrides[get_db] = override_get_db

    # Create a test client without starting the application's
    # normal lifespan, which initializes the development database.
    with TestClient(test_app) as test_client:
        yield test_client

    # Clean up after each test
    test_app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()
