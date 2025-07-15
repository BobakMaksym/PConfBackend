import abc
from typing import Any, Self

from pydantic import (
    BaseModel,
    Field,
    computed_field,
    model_validator,
    field_validator,
    field_serializer,
)

from app.rules_engine.manager import rule_manager
from app.schemas.pyobjectid import PyObjectId


class BaseComponentModel(abc.ABC, BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)

    @property
    def _id(self):
        return PyObjectId(self.id)

    class Config:
        from_attributes = True


class PowerSupply(BaseComponentModel):

    manufacturer: str
    model: str
    form_factor: str
    power: int

    # Корисні поля, допускають None
    mb_and_cpu_powersupply: str

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


# #########################################################


class Cpu(BaseComponentModel):
    manufacturer: str | None = Field(default=None)
    model: str | None = Field(default=None)

    socket: str | None = Field(default=None)
    ram_types: str | None = Field(default=None)
    igp: bool | None = Field(default=None)

    tdp: int | None = Field(default=None)
    tdp_max: int | None = Field(default=None)

    cores: int | None = Field(default=None)
    threads: int | None = Field(default=None)


class Ram(BaseComponentModel):
    manufacturer: str
    model: str

    type: str
    modules: int
    capacity: int
    speed: int

    cooling: bool | None = None
    colour: str | None = None
    lighting: bool | None = None


class Gpu(BaseComponentModel):
    manufacturer: str
    model: str
    model_gpu: str

    memory_size: int
    memory_type: str

    monitors: int | None = None

    power_consumption: int
    additional_power: str | None = None

    # декор
    fans: int | None = None
    lighting: bool | None = None


class Motherboard(BaseComponentModel):
    manufacturer: str
    model: str

    socket: str
    form_factor: str
    ram_type: str
    ram_slots: int
    m2_count: int | None = None

    chipset: str

    lighting: bool | None = None
    vrm_heatsink: bool | None = None
    wifi: bool | None = None


# #########################################################


class PcConfig(BaseModel):
    # To update the list of errors,
    # you need to call `update_errors` or `model_dump`

    id: PyObjectId | None = Field(alias="_id", default=None)
    user_id: PyObjectId

    cpu: Cpu | None = None
    ram: Ram | None = None
    motherboard: Motherboard | None = None
    gpu: Gpu | None = None
    psu: PowerSupply | None = None

    # when adding components dynamically, errors does not change
    errors: list[str | None] = Field(
        default_factory=list,
        description="list of component compatibility errors",
    )

    def update_errors(self) -> list[str]:
        """updates the list of errors"""
        self.errors = rule_manager.check_compatibility(self)
        return self.errors

    @model_validator(mode="after")
    def build_validator(self):
        """
        errors is initialized only when creating a Config object
        and does not change when dynamically adding attributes
        """
        self.update_errors()
        return self

    # class Config:
    #     json_encoders = {
    #         PyObjectId: lambda v: str(v),
    #     }


if __name__ == "__main__":

    cpu = Cpu(
        manufacturer="AMD",
        model="Ryzen 5 5600X",
        socket="AM4",
        ram_types="DDR4",
        igp=False,
        tdp=65,
        tdp_max=88,
        cores=6,
        threads=12,
    )
    ram = Ram(
        manufacturer="Corsair",
        model="Vengeance LPX",
        type="DDR5",
        modules=2,
        capacity=16,  # 16 GB total
        speed=3200,  # in MHz
    )
    gpu = Gpu(
        manufacturer="NVIDIA",
        model="GeForce RTX 3060",
        model_gpu="GA106",
        memory_size=12,  # in GB
        memory_type="GDDR6",
        power_consumption=170,  # in W
    )
    motherboard = Motherboard(
        manufacturer="MSI",
        model="B550M PRO-VDH WIFI",
        socket="AM5",
        form_factor="mATX",
        ram_type="DDR4",
        ram_slots=4,
        m2_count=2,
        chipset="B550",
    )
    psu = PowerSupply(
        manufacturer="be quiet!",
        model="Pure Power 12 M",
        form_factor="ATX",
        power=200,
        mb_and_cpu_powersupply="24+8 pin",
        plus_12v=200,  # in W
    )
