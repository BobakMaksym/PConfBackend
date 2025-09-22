from enum import StrEnum

from typesense.client import Client
from typesense.configuration import ConfigDict, NodeConfigDict
from typesense.types.collection import (
    CollectionCreateSchema,
    RegularCollectionFieldSchema,
)

from app.core.config import settings


class ComponentCollections(StrEnum):
    CPU = "cpu"
    GPU = "gpu"
    RAM = "ram"
    PSU = "psu"
    MOTHERBOARD = "motherboard"


class ComponentType(StrEnum):
    CPU = "cpu"
    GPU = "gpu"
    RAM = "ram"
    PSU = "psu"
    MOTHERBOARD = "motherboard"


schemas = {}

component_schemas = schemas
for collection in ComponentType:
    schema = CollectionCreateSchema(
        name=collection.value,
        fields=[
            RegularCollectionFieldSchema(name="id", type="string"),
            RegularCollectionFieldSchema(name="model", type="string"),
        ],
    )
    component_schemas[collection.value] = schema


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


def get_client(config_dict: ConfigDict = config_dict):
    return Client(config_dict=config_dict)
