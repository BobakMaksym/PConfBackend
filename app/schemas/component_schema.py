import abc
from bson import ObjectId
from typing import Any

from pydantic import BaseModel, Field, model_validator

from app.rules_engine import rule_registrar as registrar
from app.schemas.pyobjectid import PyObjectId


class BaseComponentModel(abc.ABC, BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)

    @property
    def _id(self):
        return ObjectId(self.id)


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


class Build(BaseModel):
    cpu: Cpu | None = None
    ram: Ram | None = None
    motherboard: Motherboard | None = None
    gpu: Gpu | None = None
    psu: PowerSupply | None = None

    model_config = {
        "validate_assignment": True,  # валідуємо й при зміні атрибутів
    }

    @model_validator(mode="after")
    def _validate_build(cls, build):
        # Запускаємо rules engine
        registrar.run(build)
        return build


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

    build = Build()
    build.cpu = cpu
    build.motherboard = motherboard
    build.ram = ram
    build.psu = psu
    build.gpu = gpu

    psu.power = 1000
    build.psu = psu
    build.ram = None
    print(build)
