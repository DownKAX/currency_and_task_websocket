from abc import ABC, abstractmethod

from app.database.db import AsyncSessionMaker
from app.repositories.user_repository import UserRepository, TaskRepository


class AbstractUnitOfWork(ABC):
    model: UserRepository #наследник должен иметь этот атрибут

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...

class UnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.session_factory = AsyncSessionMaker #наша созданная сессия, подключенная к бд, её вызов позволяет создавать отдельные сессии

    async def __aenter__(self):
        self.session = self.session_factory()
        self.model = UserRepository(self.session)
        self.task_model = TaskRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback() #не будет иметь эффекта, если commit произошёл успешно
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
