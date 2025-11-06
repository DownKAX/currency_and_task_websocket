import msgpack
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Response, HTTPException, Request, Form

from app.api.auth.dependencies import user_service, useragent_dep
from app.api.auth.exceptions import TokenExpiredException
from app.api.auth.models import Tokens, Session
from app.api.auth.redis_repository import get_session
from app.api.models.user import UserRegistrationForm, User
from app.api.auth.security import stamp_tokens, set_tokens, get_useragent, get_tokens, user_data_from_token, \
    check_session

from datetime import datetime
from passlib.hash import bcrypt

auth = APIRouter(prefix='/auth')

@auth.post('/register', response_model=User) #model_response выдаёт ошибку, если модель ответа не соответствует указанной
async def register(service: user_service, credentials: UserRegistrationForm = Form(...)):
    hashed_password = bcrypt.hash(credentials.password.get_secret_value())
    user_data = User(username=credentials.username, password=hashed_password, register_date=datetime.now())
    return await service.add_user(user=user_data)


@auth.post('/login')
async def login(response: Response, request: Request, service: user_service, credentials: OAuth2PasswordRequestForm = Depends()):
    userdata: [dict | None] = await service.get_by_username(username=credentials.username)
    if userdata is None:
        raise HTTPException(401, 'Such user does not exist')
    if not bcrypt.verify(credentials.password, userdata.get('password')):
        raise HTTPException(401, 'Wrong password')

    useragent = await get_useragent(request)
    tokens = await stamp_tokens(response, userdata, useragent)
    await set_tokens(response, tokens)

@auth.post('/check_token')
async def check_token(response: Response, request: Request, user_agent: useragent_dep):
    tokens: Tokens = await get_tokens(request)
    try:
        payload = await user_data_from_token(tokens.access_token)
    except TokenExpiredException:
        tokens = await update_tokens(response, request, user_agent)
        payload = await user_data_from_token(tokens.access_token)
    return payload

@auth.post('/update_tokens')
async def update_tokens(response: Response, request: Request, user_agent: useragent_dep):
    print('UPDATING TOKENS')
    tokens = await get_tokens(request)
    session_from_redis: Session = await get_session(tokens.refresh_token)
    if session_from_redis:
        await check_session(user_agent, session_from_redis)
        userdata = msgpack.unpackb(session_from_redis.userdata)
        token = await stamp_tokens(response, userdata, user_agent)
        return token
    else:
        raise HTTPException(status_code=401, detail="Invalid Refresh Token")

