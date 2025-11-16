from app.api.auth.models import Session
from redis_init import get_redis
from msgpack import packb, unpackb

async def add_session(userdata, refresh_token, session: Session):
    r = await get_redis()
    await r.hset(userdata, refresh_token, packb(session.model_dump()))
    await r.hset('refresh_tokens', refresh_token, userdata)

async def get_session(refresh_token: str) -> Session:
    r = await get_redis()
    userdata = await r.hget('refresh_tokens', refresh_token)
    if userdata:
        session = await r.hget(userdata, refresh_token)
        if session:
            return Session(**unpackb(session))