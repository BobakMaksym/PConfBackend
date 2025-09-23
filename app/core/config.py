from typing import Literal

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
    )

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "PConf AI"

    CREATE_NEW_SEARCH_INDEX_WHEN_RESTART: bool

    # JWT
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # CORS
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl]

    # Database
    MONGO_CONNECTION_STRING: str
    DATABASE: str

    # Typesense
    TYPESENSE_API_KEY: str
    TYPESENSE_HOST: str
    TYPESENSE_PORT: int
    TYPESENSE_PROTOCOL: str

    # Agents
    WORKFLOW_NAME: str = "AI Chat"

    # Logger
    LOG_LEVEL: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]


settings = Settings()  # type: ignore
