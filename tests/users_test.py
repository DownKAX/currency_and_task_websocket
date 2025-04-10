import pytest
from httpx import AsyncClient, ASGITransport
import pytest_asyncio
import asyncio
import os
from alembic.config import Config
from alembic import command
from app.core.config import settings

from main import app


@pytest_asyncio.fixture(name='client')
async def async_client():
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture(autouse=True)
async def alembic():
    alembic_config = Config('alembic_test.ini')
    await asyncio.to_thread(command.upgrade, alembic_config, 'head') #выполняем асинхронно синхронные функции
    yield
    await asyncio.to_thread(command.downgrade, alembic_config, 'base')


@pytest.mark.asyncio
async def test_login_correct(client):
    response = await client.post("/auth/login", data={"username": "user", "password": "user123456"})
    assert response.status_code == 200
    assert response.json() == {"message": 'Logged in successfully'}

@pytest.mark.asyncio
async def test_login_wrong_password(client):
    response = await client.post("/auth/login", data={"username": "user", "password": "user323"})
    assert response.status_code == 401
    assert response.json() == {"detail": 'Wrong password'}

@pytest.mark.asyncio
async def test_login_non_existing_user(client):
    response = await client.post("/auth/login", data={"username": "someone", "password": "user323"})
    assert response.status_code == 401
    assert response.json() == {"detail": 'Such user does not exist'}

@pytest.mark.asyncio
async def test_register_success(client):
    response = await client.post("/auth/register", json={"username": "mod", "password": "admin123456", "confirm_password": "admin123456"})
    assert response.status_code == 200
    assert "username" in response.json()

@pytest.mark.asyncio
async def test_register_with_already_taken_name(client):
    response = await client.post("/auth/register", json={"username": "admin", "password": "admin123456", "confirm_password": "admin123456"})
    assert response.status_code == 401
    assert response.json() == {"detail": "User with such name already exists"}

@pytest.mark.asyncio
async def test_register_passwords_doesnt_match(client):
    response = await client.post("/auth/register", json={"username": "admin1", "password": "admin123456", "confirm_password": "admin1234567"})
    assert response.status_code == 401
    assert response.json() == {"detail": 'Passwords do not match'}

@pytest.mark.asyncio
async def test_register_with_short_password(client):
    response = await client.post("/auth/register", json={"username": "admin1","password": "adm","confirm_password": "adm"})
    assert response.status_code == 401
    assert response.json() == {"detail": 'Length must be between 8 and 64'}

@pytest.mark.asyncio
async def test_register_with_long_password(client):
    response = await client.post("/auth/register", json={"username": "admin1","password": "adm" * 100,"confirm_password": "adm" * 100})
    assert response.status_code == 401
    assert response.json() == {"detail": 'Length must be between 8 and 64'}






