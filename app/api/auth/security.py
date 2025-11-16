import os

import msgpack
from dotenv import load_dotenv
path = dotenv_path=os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path=path)
from datetime import datetime, UTC, timedelta

import jwt
from fastapi import Request, Response, HTTPException

from app.api.auth.exceptions import TokenNotFoundException, TokenExpiredException
from app.api.auth.models import Session, SessionForRedis, Tokens
from app.api.auth.redis_repository import add_session
from app.core.config import settings


async def stamp_tokens(response: Response, userdata, useragent):
    if userdata.get('register_date'): userdata.pop('register_date')
    if userdata.get('password'): userdata.pop('password')
    session = await create_session(useragent, userdata)
    await add_session(userdata=userdata.get('username'),
                      refresh_token=session.refresh_token,
                      session=session.session)
    session_token = await create_access_token(userdata)
    for_return = Tokens(access_token=session_token, refresh_token=session.refresh_token)
    await set_tokens(response, tokens=for_return)
    return for_return

async def get_tokens(request: Request):
    session_token = request.cookies.get('session_token')
    refresh_token = request.cookies.get('refresh_token')
    if refresh_token:
        return Tokens(refresh_token=refresh_token, access_token=session_token)
    else:
        raise TokenNotFoundException

async def set_tokens(response: Response, tokens: Tokens):
    response.set_cookie(key='session_token', value=tokens.access_token)
    response.set_cookie(key='refresh_token', value=tokens.refresh_token)

async def create_access_token(data: dict) -> str:
    data['exp'] = datetime.now(UTC) + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRATION)
    return jwt.encode(data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def create_session(useragent, userdata) -> SessionForRedis:
    refresh_token = hex(8)
    userdata = msgpack.packb(userdata)
    session = Session(userdata=userdata, useragent=useragent)
    return SessionForRedis(refresh_token=refresh_token, session=session)

async def get_useragent(request: Request):
    useragent: str = request.headers.get('User-Agent')
    return useragent


async def user_data_from_token(token: str):
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Token")

async def check_session(user_agent, session_from_redis: Session):
    if session_from_redis.useragent != user_agent:
        raise HTTPException(status_code=401, detail="Invalid Refresh Token")
    if session_from_redis.exp < datetime.now(UTC).timestamp():
        raise HTTPException(status_code=401, detail="Expired Token")
    return True