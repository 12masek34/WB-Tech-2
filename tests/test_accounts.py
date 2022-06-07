import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from models.database import Base, AsyncDatabaseSession
from config import Config

engine = create_engine(
    Config.TEST_DB_CONFIG, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[AsyncDatabaseSession] = override_get_db

client = TestClient(app)


def test_create_user():
    response = client.post(
        'http://0.0.0.0:8000/api/v1/users/registration',
        json={
            "username": "string4",
            "email": "user4@example.com",
            "password1": "string",
            "password2": "string"
        }
    )
    print(response.json())
    print(response.status_code)
