from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Cookie, Response, HTTPException

from app.api.models.user import UserRegistrationForm, User
from app.service.users_service import UsersService
from app.utils.unitofwork import AbstractUnitOfWork, UnitOfWork
from app.core.security import create_access_token

from datetime import datetime
from passlib.hash import bcrypt

auth = APIRouter(prefix='/auth')


async def get_user_service(uow: AbstractUnitOfWork = Depends(UnitOfWork)) -> UsersService: #тут depends создаёт экзмемпляр класса
    return UsersService(uow)


@auth.post('/register', response_model=User) #model_response выдаёт ошибку, если модель ответа не соответствует указанной
async def register(credentials: UserRegistrationForm, user_service: UsersService = Depends(get_user_service)):
    hashed_password = bcrypt.hash(credentials.password.get_secret_value())
    user_data = User(username=credentials.username, password=hashed_password, register_date=datetime.now())
    return await UsersService.add_user(self=user_service, user=user_data)


@auth.post('/login')
async def login(response: Response, credentials: OAuth2PasswordRequestForm = Depends(), user_service: UsersService = Depends(get_user_service)):
    user: [dict | None] = await UsersService.get_by_username(self=user_service, username=credentials.username)
    if user is None:
        raise HTTPException(401, 'Such user does not exist')
    if not bcrypt.verify(credentials.password, user.get('password')):
        raise HTTPException(401, 'Wrong password')

    session_token = await create_access_token(user)
    response.set_cookie(key='session_token', value=session_token, secure=True, httponly=True)
    return {'message': 'Logged in successfully'}


