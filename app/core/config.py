from typing import Literal

from decouple import config
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


LOG_LEVELS = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
    ]
    PROJECT_NAME: str = "PConf AI"

    # Database
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)
    DATABASE: str = config("DATABASE", cast=str)

    # Agents
    WORKFLOW_NAME: str = "AI Chat"

    LOG_LEVEL: LOG_LEVELS = config("LOG_LEVEL")

    class Config:
        case_sensitive = True


settings = Settings()
