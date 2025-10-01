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
# for collection in ComponentType:
#     schema = CollectionCreateSchema(
#         name=collection.value,
#         fields=[
#             RegularCollectionFieldSchema(name="id", type="string"),
#             RegularCollectionFieldSchema(name="model", type="string"),
#         ],
#     )
#     component_schemas[collection.value] = schema


common_fields: list[RegularCollectionFieldSchema] = [
    {"name": "id", "type": "string"},
    {"name": "model", "type": "string", "optional": True},
    {"name": "manufacturer", "type": "string", "optional": True},
]


schema_cpu = CollectionCreateSchema(
    name=ComponentType.CPU,
    fields=[
        *common_fields,
        {"name": "socket", "type": "string", "optional": True},
        {"name": "ram_types", "type": "string", "optional": True},
        {"name": "igp", "type": "bool", "optional": True},
        {"name": "tdp", "type": "int32", "optional": True},
        {"name": "tdp_max", "type": "int32", "optional": True},
        {"name": "cores", "type": "int32", "optional": True},
        {"name": "threads", "type": "int32", "optional": True},
    ],
)

schema_ram = CollectionCreateSchema(
    name=ComponentType.RAM,
    fields=[
        *common_fields,
        {"name": "type", "type": "string", "optional": True},
        {"name": "modules", "type": "int32", "optional": True},
        {"name": "capacity", "type": "int32", "optional": True},
        {"name": "speed", "type": "int32", "optional": True},
        {"name": "cooling", "type": "bool", "optional": True},
        {"name": "colour", "type": "string", "optional": True},
        {"name": "lighting", "type": "bool", "optional": True},
    ],
)

schema_gpu = CollectionCreateSchema(
    name=ComponentType.GPU,
    fields=[
        *common_fields,
        {"name": "model_gpu", "type": "string", "optional": True},
        {"name": "memory_size", "type": "int32", "optional": True},
        {"name": "memory_type", "type": "string", "optional": True},
        {"name": "monitors", "type": "int32", "optional": True},
        {"name": "power_consumption", "type": "int32", "optional": True},
        {"name": "additional_power", "type": "string", "optional": True},
        {"name": "fans", "type": "int32", "optional": True},
        {"name": "lighting", "type": "bool", "optional": True},
    ],
)

schema_motherboard = CollectionCreateSchema(
    name=ComponentType.MOTHERBOARD,
    fields=[
        *common_fields,
        {"name": "socket", "type": "string", "optional": True},
        {"name": "form_factor", "type": "string", "optional": True},
        {"name": "ram_type", "type": "string", "optional": True},
        {"name": "ram_slots", "type": "int32", "optional": True},
        {"name": "m2_count", "type": "int32", "optional": True},
        {"name": "chipset", "type": "string", "optional": True},
        {"name": "lighting", "type": "bool", "optional": True},
        {"name": "vrm_heatsink", "type": "bool", "optional": True},
        {"name": "wifi", "type": "bool", "optional": True},
    ],
)

schema_psu = CollectionCreateSchema(
    name=ComponentType.PSU,
    fields=[
        *common_fields,
        {"name": "form_factor", "type": "string", "optional": True},
        {"name": "power", "type": "int32", "optional": True},
        {"name": "mb_and_cpu_powersupply", "type": "string", "optional": True},
        {"name": "efficiency", "type": "int32", "optional": True},
        {"name": "plus_12v", "type": "int32", "optional": True},
        {"name": "cable_system", "type": "string", "optional": True},
        {"name": "certification", "type": "string", "optional": True},
        {"name": "cooling_system", "type": "string", "optional": True},
        {"name": "fan_bearing", "type": "string", "optional": True},
        {"name": "manufacturers_warranty", "type": "int32", "optional": True},
        {"name": "dimensions", "type": "string", "optional": True},
    ],
)

component_schemas = {
    ComponentCollections.CPU.value: schema_cpu,
    ComponentCollections.GPU.value: schema_gpu,
    ComponentCollections.MOTHERBOARD.value: schema_motherboard,
    ComponentCollections.RAM.value: schema_ram,
    ComponentCollections.PSU.value: schema_psu,
}


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
