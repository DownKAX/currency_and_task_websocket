from datetime import datetime, UTC, timedelta
import os
from dotenv import load_dotenv
path = dotenv_path=os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path=path)
from pydantic import BaseModel, Field
from app.core.config import settings


class Session(BaseModel):
    userdata: bytes
    useragent: str
    exp: float = Field(default_factory=lambda: (datetime.now(UTC) + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRATION)).timestamp())

class SessionForRedis(BaseModel):
    session: Session
    refresh_token: str

class Tokens(BaseModel):
    access_token: str
    refresh_token: str