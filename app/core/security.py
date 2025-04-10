import jwt
import datetime
from fastapi import HTTPException

from app.core.config import settings

async def create_access_token(data: dict) -> str:
    data.pop('register_date')
    data.pop('password')
    data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    return jwt.encode(data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def user_data_from_token(token: str):
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired Signature")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Token")



