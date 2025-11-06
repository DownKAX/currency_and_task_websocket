from app.api.models.user import User
from app.api.models.tasks import Task
from app.utils.unitofwork import AbstractUnitOfWork
from app.utils.websocket import WebsocketUtil
from app.service.data_validators import unique_check, permission_check, existing_check

from datetime import datetime


class UsersService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow #имеет атрибут model(является табилицей в бд), который является репозиторием, имеющим методы CRUD и другие. Также имеет атрибут session, который уже подключён к нашей .db

    async def add_user(self, user: User) -> User:
        user_dict: dict = user.model_dump() #преобразуем в dict
        async with self.uow: #используем uow, в котором реализованы aexit, который предотващает ошибки и делает rollback()
            user_from_db = await self.uow.model.add_one(user_dict) #метод возвращает добавленные данные, записываем их в переменную
            await unique_check(user_from_db, 'User')
            user_to_return = User.model_validate(user_from_db.__dict__) #проверяем user_from_db на то, что он соответсвует модели User, если успешно - user_to_return становится экземпляром модели User, в противном случае ошибка(лишние ключи игнорируются)
            await self.uow.commit() #если код не дошёл до этой строчки и где-то произошла ошибка, то вызовется метод, который определил в созданном контектсном менеджере __aexit__ и произойдёт rollback()
            return user_to_return #можно использовать в ответе пользователю или логах

    async def get_users(self):
        async with self.uow:
            data = await self.uow.model.show_all_data()
            return [User.model_validate(user) for user in data] #проверяем каждую запись и выводим данные

    async def get_by_username(self, username):
        async with self.uow:
            data = await self.uow.model.find_one(username=username)
            if data is not None: data = {'username': data.username, 'password': data.password, 'register_date': data.register_date, 'role': data.role}
            return data

class TaskService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def add_task(self, task: Task, username: str, util: WebsocketUtil):
        task_dict: dict = task.model_dump()
        task_dict.update({'created_by': username, 'date_of_start': datetime.now()})
        async with self.uow:
            task_from_db = await self.uow.task_model.add_one(task_dict); await unique_check(task_from_db, 'Task')
            task_to_return = Task.model_validate(task_from_db.__dict__)
            await self.uow.commit()
            await util.on_task_event(task_title=task_to_return.title, username=username, action='created the task')
            return task_to_return

    async def get_tasks(self):
        async with self.uow:
            data = await self.uow.task_model.show_all_data()
            return [Task.model_validate(task) for task in data]

    async def update_task(self, id: int, username: str, util: WebsocketUtil,action='updated', **values):
        async with self.uow:
            values = {x: y for x, y in values.items() if y is not None}
            updated_data = await self.uow.task_model.edit_one(id=id, **values)
            await existing_check(updated_data, "Task")
            await self.uow.commit()
            await util.on_task_event(task_title=updated_data.title, username=username, action=f'{action} the task')
            return updated_data

    async def delete_task(self, id: int, role: str, username: str, util: WebsocketUtil):
        async with self.uow:
            await permission_check(role, acceptable_roles=('moderator', 'admin'))
            deleted_data = await self.uow.task_model.delete_one(id); await existing_check(deleted_data, 'Task')
            deleted_data = Task.model_validate(deleted_data.__dict__)
            await util.on_task_event(task_title=deleted_data.title, username=username, action='deleted the task')
            await self.uow.commit()
            return deleted_data
