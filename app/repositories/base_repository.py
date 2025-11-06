from abc import ABC, abstractmethod

import sqlalchemy.exc
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound, IntegrityError

class AbstractBaseRepository(ABC):
    @abstractmethod
    async def add_one(self, data):
        raise NotImplementedError

    @abstractmethod
    async def show_all_data(self, **filter_by):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, **filter_by):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id: int, **filter_by):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int):
        raise NotImplementedError

class Repository(AbstractBaseRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data):
        query = insert(self.model).values(**data).returning(self.model) #query - сгенерированный SQL-запрос вставки в модель(таблицу), выполняется, возвращая добавленные данные
        try:
            result = await self.session.scalar(query) #асинхронно выполняем SQL-запрос
            return result #возвращаем добавленные данные(одну строку или ошибка)
        except IntegrityError: #при случае нарушения уникальности данных
            return None

    async def show_all_data(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all() #возвращаем все данные, которые есть

    async def find_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            result = result.scalar_one()
            return result
        except NoResultFound:
            return None

    async def edit_one(self, id: int, **values):
        query = update(self.model).where(self.model.id==id).values(**values).returning(self.model)
        result = await self.session.execute(query)
        try:
            result = result.scalar_one()
            return result
        except NoResultFound:
            return None


    async def delete_one(self, id: int):
        query = delete(self.model).where(self.model.id == id).returning(self.model)
        try:
            result = await self.session.execute(query)
            return result.scalar_one()
        except NoResultFound:
            return None


