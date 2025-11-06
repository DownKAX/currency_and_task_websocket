import pytest
from httpx import AsyncClient, ASGITransport
import pytest_asyncio
import asyncio
import os
from pathlib import Path
from app.core.config import settings
from alembic.config import Config
from alembic import command

from main import app
from app.api.auth.security import create_access_token


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

@pytest_asyncio.fixture(autouse=False, name='moderator_session_token')
async def create_moderator_token():
    user = {'username': 'moderator', 'password': "moderator123456", 'register_date': None, 'role': 'moderator'}
    token = await create_access_token(user)
    return token

@pytest_asyncio.fixture(autouse=False, name='admin_session_token')
async def create_admin_token():
    user = {'username': 'admin', 'password': "admin123456", 'register_date': None, 'role': 'admin'}
    token = await create_access_token(user)
    return token


class TestTasks:
    @pytest.mark.asyncio
    async def test_create_correct(self, client, user_session_token): #используем name, которое возвращает значение функции create_user_token
        response = await client.post("/tasks/create_task", json={"title": "todoTitldd1e5", "description": "todoDescription"}, cookies={'session_token': user_session_token, 'refresh_token': '0x9'})
        assert 'title' in response.json()
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_create_unique_error(self, user_session_token, client):
        response = await client.post("/tasks/create_task", json={"title": "Task 1", "description": "todoDescription"}, cookies={'session_token': user_session_token, 'refresh_token': '0x9'})
        assert response.json() == {"detail": 'Task with such name already exists'}
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_correct_delete_task(self, moderator_session_token, client):
        response = await client.delete("/tasks/delete_task", params={'id': 1}, cookies={'session_token': moderator_session_token, 'refresh_token': '0x9'})
        assert response.status_code == 200
        assert 'title' in response.json()

    @pytest.mark.asyncio
    async def test_non_existing_delete_task(self, moderator_session_token, client):
        response = await client.delete("/tasks/delete_task", params={'id': 5}, cookies={'session_token': moderator_session_token, 'refresh_token': '0x9'})
        assert response.status_code == 401
        assert response.json() == {"detail": "Such Task does not exist"}

    @pytest.mark.asyncio
    async def test_update_task_correct_title_edit(self, moderator_session_token, client):
        response = await client.put("/tasks/update_task", params={'id': 1}, json={'title': 'updatedToDo'}, cookies={'session_token': moderator_session_token, 'refresh_token': '0x9'})
        assert response.status_code == 200
        assert response.json()['title'] == 'updatedToDo'

    @pytest.mark.asyncio
    async def test_update_task_correct_description_edit(self, moderator_session_token, client):
        response = await client.put("/tasks/update_task", params={'id': 1}, json={'description': 'updatedDesc'}, cookies={'session_token': moderator_session_token, 'refresh_token': '0x9'})
        assert response.status_code == 200
        assert response.json()['description'] == 'updatedDesc'

    @pytest.mark.asyncio
    async def test_update_task_correct_description_and_tilte_edit(self, moderator_session_token, client):
        response = await client.put("/tasks/update_task", params={'id': 1}, json={'title': 'updatedToDo', 'description': 'updatedDesc'},
                              cookies={'session_token': moderator_session_token, 'refresh_token': '0x9'})
        assert response.status_code == 200
        assert response.json()['description'] == 'updatedDesc'
        assert response.json()['title'] == 'updatedToDo'

    @pytest.mark.asyncio
    async def test_update_task_no_data(self, moderator_session_token, client):
        response = await client.put("/tasks/update_task", params={'id': 1}, cookies={'session_token': moderator_session_token, 'refresh_token': '0x9'})

        assert response.status_code == 400
        assert response.json() == {'detail': 'You must provide at least one parameter'}

    @pytest.mark.asyncio
    async def test_update_non_existing_task(self, moderator_session_token, client):
        response = await client.put("/tasks/update_task", params={'id': 6}, json={'title': 'updatedToDo'}, cookies={'session_token': moderator_session_token, 'refresh_token': '0x9'})
        assert response.status_code == 401
        assert response.json() == {"detail": "Such Task does not exist"}

    @pytest.mark.asyncio
    async def test_finish_task_correct(self, moderator_session_token, client):
        response = await client.put("/tasks/finish_task", params={'id': 1}, cookies={'session_token': moderator_session_token, 'refresh_token': '0x9'})
        assert response.status_code == 200
        assert response.json()['date_of_finish'] is not None

    @pytest.mark.asyncio
    async def test_finish_task_non_existing(self, moderator_session_token, client):
        response = await client.put("/tasks/finish_task", params={'id': 6}, cookies={'session_token': moderator_session_token, 'refresh_token': '0x9'})
        assert response.status_code == 401
        assert response.json() == {"detail": "Such Task does not exist"}
