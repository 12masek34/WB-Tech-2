import asyncio

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from config import Config
from main import app
from models.database import get_db, AsyncDatabaseSession


def override_get_db():
    db = AsyncDatabaseSession()
    db.init(Config.TEST_DB_CONFIG)
    return db


app.dependency_overrides[get_db] = override_get_db



@pytest.fixture(autouse=True, scope="module")
async def create_test_database():
    db = override_get_db()
    await db.create_all()
    yield
    await db.drop_all()


@pytest.mark.anyio
async def test_root():

    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000/api/v1/users/") as ac:
        response = await ac.post("registration", json={
            "username": "string",
            "email": "user@example.com",
            "password1": "string",
            "password2": "string"
        })
        print(response.json())

