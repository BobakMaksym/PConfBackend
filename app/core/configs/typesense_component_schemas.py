from bson import ObjectId
from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from pydantic_extra_types.mongo_object_id import MongoObjectId


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
    manufacturer: str | None = None
    model: str | None = None


class CpuIndexSchema(BaseIndexSchema):
    socket: str | None = None
    ram_types: str | None = None
    igp: bool | None = None
    tdp: int | None = None
    tdp_max: int | None = None
    cores: int | None = None
    threads: int | None = None


class RamIndexSchema(BaseIndexSchema):
    type: str | None = None
    modules: int | None = None
    capacity: int | None = None
    speed: int | None = None

    cooling: bool | None = None
    colour: str | None = None
    lighting: bool | None = None


class GpuIndexSchema(BaseIndexSchema):
    model_gpu: str | None = None

    memory_size: int | None = None
    memory_type: str | None = None

    monitors: int | None = None

    power_consumption: int | None = None
    additional_power: str | None = None

    fans: int | None = None
    lighting: bool | None = None


class MotherboardIndexSchema(BaseIndexSchema):
    socket: str | None = None
    form_factor: str | None = None
    ram_type: str | None = None
    ram_slots: int | None = None
    m2_count: int | None = None

    chipset: str | None = None

    lighting: bool | None = None
    vrm_heatsink: bool | None = None
    wifi: bool | None = None


class SsdIndexSchema(BaseIndexSchema):
    form_factor: str

    volume: int | None = None
    read_speed: int | None = None
    write_speed: int | None = None

    controller: str | None = None
    interface_m2: str | None = None
    memory_type: str | None = None
    nvme: bool | None = None
    radiator: bool | None = None


class PowerSupplyIndexSchema(BaseIndexSchema):
    form_factor: str | None = None
    power: int | None = None

    mb_and_cpu_powersupply: str | None = None

    efficiency: int | None = None
    plus_12v: int | None = None

    pci_e_8pin_6_2: int | None = None
    pci_e_16pin: int | None = None
    pci_e_6pin: int | None = None
    pci_e_8pin: int | None = None

    # декор
    cable_system: str | None = None
    certification: str | None = None
    cooling_system: str | None = None
    fan_bearing: str | None = None

    # інфа
    manufacturers_warranty: int | None = None
    dimensions: str | None = None


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
