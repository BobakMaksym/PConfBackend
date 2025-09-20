import logging
from typing import Literal

from pika import ConnectionParameters, PlainCredentials
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typesense.configuration import ConfigDict, NodeConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
    )

    # MongoDB
    MONGO_CONNECTION_STRING: str
    MONGO_DATABASE: str

    # Typesense
    TYPESENSE_API_KEY: str
    TYPESENSE_HOST: str
    TYPESENSE_PORT: int
    TYPESENSE_PROTOCOL: str

    # Rabbit
    RABBIT_HOST: str
    RABBIT_PORT: int
    RABBIT_USERNAME: str
    RABBIT_PASSWORD: str
    RABBIT_EXCHANGE: str = Field(default="")  # default AMQP direct
    RABBIT_ROUTING_KEY: str

    # Logger
    LOG_LEVEL: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]


config = Config()  # type: ignore


def configure_logging(level: int = logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(funcName)20s %(module)s:%(lineno)d %(levelname)-8s - %(message)s\n",
    )


rabbit_connection_params = ConnectionParameters(
    host=config.RABBIT_HOST,
    port=config.RABBIT_PORT,
    credentials=PlainCredentials(
        username=config.RABBIT_USERNAME,
        password=config.RABBIT_PASSWORD,
    ),
)

typesense_config = ConfigDict(
    nodes=[
        NodeConfigDict(
            host=config.TYPESENSE_HOST,
            port=config.TYPESENSE_PORT,
            protocol=config.TYPESENSE_PROTOCOL,
        )
    ],
    api_key=config.TYPESENSE_API_KEY,
    connection_timeout_seconds=5,
)
