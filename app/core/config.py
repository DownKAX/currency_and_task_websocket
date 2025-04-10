from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ConfigDict
from pathlib import Path



class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8")

settings = Settings()