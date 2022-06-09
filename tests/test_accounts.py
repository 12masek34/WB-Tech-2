import pytest
import pytest_asyncio
from httpx import AsyncClient
from starlette import status

from accounts.auth import get_password_hash
from config import Config
from main import app
from models.database import get_db, AsyncDatabaseSession
from services.CRUD_user import create_user


@pytest_asyncio.fixture
async def db():
    db = AsyncDatabaseSession()
    db.init(Config.TEST_DB_CONFIG)
    await db.create_all()
    app.dependency_overrides[get_db] = lambda: db
    yield db
    await db.drop_all()

#
# @pytest_asyncio.fixture
# async def create_test_user(db):




@pytest.mark.asyncio
async def test_create_user_positive(db):
    async with AsyncClient(app=app, base_url='http://0.0.0.0:8000/api/v1/users/') as ac:
        response = await ac.post('registration', json={
            'username': 'string',
            'email': 'user@example.com',
            'password1': 'string',
            'password2': 'string'
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert 'username' in response.json()
        assert 'email' in response.json()
        assert 'full_name' in response.json()
        assert 'disabled' in response.json()


@pytest.mark.asyncio
async def test_create_user_negative(db):
    async with AsyncClient(app=app, base_url='http://0.0.0.0:8000/api/v1/users/') as ac:
        response = await ac.post('registration', json={
            # 'username': 'string',
            'email': 'user@example.com',
            'password1': 'string',
            'password2': 'string'
        })

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {'detail': [{'loc': ['body', 'username'], 'msg': 'field required',
                                           'type': 'value_error.missing'}]}

    async with AsyncClient(app=app, base_url='http://0.0.0.0:8000/api/v1/users/') as ac:
        response = await ac.post('registration', json={
            'username': 'string',
            # 'email': 'user@example.com',
            'password1': 'string',
            'password2': 'string'
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async with AsyncClient(app=app, base_url='http://0.0.0.0:8000/api/v1/users/') as ac:
        response = await ac.post('registration', json={
            'username': 'string',
            'email': 'user@example.com',
            # 'password1': 'string',
            'password2': 'string'
        })

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == {'detail': [{'loc': ['body', 'password1'], 'msg': 'field required',
                                               'type': 'value_error.missing'}]}

        async with AsyncClient(app=app, base_url='http://0.0.0.0:8000/api/v1/users/') as ac:
            response = await ac.post('registration', json={
                'username': 'string',
                'email': 'user@example.com',
                'password1': 'string',
                # 'password2': 'string'
            })

            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
            assert response.json() == {'detail': [{'loc': ['body', 'password2'], 'msg': 'field required',
                                                   'type': 'value_error.missing'}]}


@pytest.mark.asyncio
async def test_create_token_positive(db):

    async with AsyncClient(app=app, base_url='http://0.0.0.0:8000/api/v1/users/') as ac:
        response = await ac.post('token', data={
            'username': 'test_user',
            'password': 'test_password'
        })

        user = await create_user(db, username='test_user', email='test@test.com', hashed_password='test_password')
        print(user)
        async with AsyncClient(app=app, base_url='http://0.0.0.0:8000/api/v1/users/') as ac:
            response = await ac.post('token', data={
                'username': 'test_user',
                'password': 'test_password'
            })
        print(response.status_code)
        print(response.json())