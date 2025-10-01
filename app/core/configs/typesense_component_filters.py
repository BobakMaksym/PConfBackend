from enum import StrEnum
from typing import Any

from bson import ObjectId
from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    SerializationInfo,
    field_validator,
    model_serializer,
)
from pydantic_extra_types.mongo_object_id import MongoObjectId


class StrBool(StrEnum):
    TRUE = "true"
    FALSE = "false"
    NONE = "none"


class BaseIndexSchema(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=True,
        use_enum_values=True,
        extra="allow",
    )

    id: MongoObjectId = Field(
        validation_alias=AliasChoices("id", "_id"),
        serialization_alias="id",
    )
    manufacturer: str = ""
    model: str = ""

    @field_validator("*", mode="before")
    def normalize_bool_none(cls, v: Any) -> Any:
        """normalizes Boolean values for typesense"""

        if isinstance(v, bool):
            return {True: "true", False: "false", None: "none"}[v]
        return v

    @model_serializer(mode="wrap")
    def drop_empty_values(self, handler, info: SerializationInfo):
        """"""

        data = handler(self)

        keys = list(data.keys())

        if info.exclude_none:
            # deletes placeholder values
            for i in range(len(keys) - 1, -1, -1):
                v = data[keys[i]]
                if v in (-1, "", StrBool.NONE):
                    del data[keys[i]]
        else:
            # replacement of placeholders with standard data types
            for i in range(len(keys) - 1, -1, -1):
                v = data[keys[i]]

                if v in StrBool:
                    data[keys[i]] = {"true": True, "false": False, "none": None}[v]

                if v in (-1, ""):
                    data[keys[i]] = None

        return data


"""
str: ""
bool: "None", "True", "False"
int: -1 -> None
"""


class CpuIndexSchema(BaseIndexSchema):
    socket: str = ""
    ram_types: str = ""
    igp: StrBool | None | bool = StrBool.NONE
    tdp: int = -1
    tdp_max: int = -1
    cores: int = -1
    threads: int = -1


class RamIndexSchema(BaseIndexSchema):
    type: str = ""
    modules: int = -1
    capacity: int = -1
    speed: int = -1

    cooling: StrBool | None | bool = StrBool.NONE
    colour: str = ""
    lighting: StrBool | None | bool = StrBool.NONE


class GpuIndexSchema(BaseIndexSchema):
    model_gpu: str = ""

    memory_size: int = -1
    memory_type: str = ""

    monitors: int = -1

    power_consumption: int = -1
    additional_power: str = ""

    fans: int = Field(default=-1)
    lighting: StrBool | None | bool = StrBool.NONE


class MotherboardIndexSchema(BaseIndexSchema):
    socket: str = ""
    form_factor: str = ""
    ram_type: str = ""
    ram_slots: int = -1
    m2_count: int = -1

    chipset: str = ""

    lighting: StrBool | None | bool = StrBool.NONE
    vrm_heatsink: StrBool | None | bool = StrBool.NONE
    wifi: StrBool | None | bool = StrBool.NONE


class PowerSupplyIndexSchema(BaseIndexSchema):
    form_factor: str = ""
    power: int = -1

    # Корисні поля, допускають None
    mb_and_cpu_powersupply: str = ""

    efficiency: int = -1
    plus_12v: int = -1

    pci_e_8pin_6_2: int = -1
    pci_e_16pin: int = -1
    pci_e_6pin: int = -1
    pci_e_8pin: int = -1

    # декор
    cable_system: str = ""
    certification: str = ""
    cooling_system: str = ""
    fan_bearing: str = ""

    # інфа
    manufacturers_warranty: int = -1
    dimensions: str = ""


if __name__ == "__main__":
    from bson import ObjectId
    from pprint import pprint

    cpu = CpuIndexSchema(id=ObjectId(), model="amd")

    pprint(cpu)
    print()

    res = cpu.model_dump()
    pprint(res)
    print()

    res = cpu.model_dump(exclude_none=True)
    pprint(res)
    print()
