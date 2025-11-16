from fastapi import Depends
from typing import Annotated

from app.api.auth.security import get_useragent
from app.service.users_service import UsersService
from app.utils.unitofwork import AbstractUnitOfWork, UnitOfWork

async def get_user_service(uow: AbstractUnitOfWork = Depends(UnitOfWork)) -> UsersService: #тут depends создаёт экзмемпляр класса
    return UsersService(uow)

user_service = Annotated[UsersService, Depends(get_user_service)]
useragent_dep = Annotated[str, Depends(get_useragent)]