from enum import StrEnum
from logging import getLogger

from typesense.configuration import ConfigDict, NodeConfigDict

from app.core.config import settings


class ComponentCollections(StrEnum):
    CPU = "cpu"
    GPU = "gpu"
    RAM = "ram"
    PSU = "psu"
    MOTHERBOARD = "motherboard"


schemas = {}
for collection in ComponentCollections:
    schema = {
        "name": collection,
        "fields": [
            {"name": "id", "type": "string"},
            {"name": "model", "type": "string"},
        ],
    }
    schemas[collection] = schema


config_dict = ConfigDict(
    nodes=[
        NodeConfigDict(
            host=settings.TYPESENSE_HOST,
            port=settings.TYPESENSE_PORT,
            protocol=settings.TYPESENSE_PROTOCOL,
        )
    ],
    api_key=settings.TYPESENSE_API_KEY,
    connection_timeout_seconds=5,
)
