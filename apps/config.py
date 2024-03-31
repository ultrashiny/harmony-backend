from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from typing import List
from decouple import config

class CommonSettings(BaseSettings):
    APP_NAME: str = "Harmony"
    DEBUG_MODE: bool = True

class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8001

class DatabaseSettings(BaseSettings):
    DB_URL: str = config("DB_URL", cast=str)
    DB_NAME: str = config("DB_NAME", cast=str)

class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    class Config:
        case_sensitive: True

settings = Settings()