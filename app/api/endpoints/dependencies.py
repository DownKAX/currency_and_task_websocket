from fastapi import Depends
from typing import Annotated

from app.service.users_service import TaskService
from app.utils.unitofwork import AbstractUnitOfWork, UnitOfWork


async def get_task_service(uow: AbstractUnitOfWork = Depends(UnitOfWork)) -> TaskService:
    return TaskService(uow)

task_service = Annotated[TaskService, Depends(get_task_service)]