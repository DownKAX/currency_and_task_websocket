import pytest
from httpx import AsyncClient, ASGITransport
import pytest_asyncio
import unittest
from unittest.mock import patch, AsyncMock
from alembic.config import Config
from alembic import command
import asyncio

from main import app
from app.core.security import create_access_token
from app.core.config import settings
from app.utils.external_api import ExternalAPI


@pytest_asyncio.fixture(name='client') #стандартное создание асинхронного клиента для теста
async def async_client():
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture(autouse=True)
async def alembic():
    alembic_config = Config('alembic_test.ini')
    await asyncio.to_thread(command.upgrade, alembic_config, 'head') #выполняем асинхронно синхронные функции
    yield
    await asyncio.to_thread(command.downgrade, alembic_config, 'base')


@pytest_asyncio.fixture(autouse=False, name='user_session_token') #указываем имя, которое будет возвращать значение функции
async def create_user_token():
    user = {'username': 'user', 'password': "user123456", 'register_date': None, 'role': 'user'}
    token = await create_access_token(user)
    return token


@pytest.mark.asyncio
async def test_get_codes_correct(client, user_session_token):
    with patch('app.utils.external_api.ExternalAPI.get_currency_codes', new_callable=AsyncMock) as mock_get_currency_codes:
        mock_get_currency_codes.return_value = 'mock_list'
        response = await client.get('/currency/get_currency_codes', headers={"Cookie": f'session_token={user_session_token}'})
        assert response.status_code == 200
        assert 'currencies' in response.json()  # конечная точка(в currency endpoints) возвращает {'currencies': get_currency_codes}


@pytest.mark.asyncio
async def test_get_codes_no_token(client):
    with patch('app.utils.external_api.ExternalAPI.get_currency_codes', new_callable=AsyncMock) as mock_get_currency_codes:
        mock_get_currency_codes.return_value = {'currencies': ['mock_code']}
        response = await client.get('/currency/get_currency_codes')
        print(response)
        assert response.status_code == 422
        assert 'error' in response.json()