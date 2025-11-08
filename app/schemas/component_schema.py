from pydantic import Field

from app.schemas.base import BaseDbSchema


class BaseDbComponentSchema(BaseDbSchema):
    manufacturer: str
    model: str


class CpuSchema(BaseDbComponentSchema):
    socket: str | None = Field(default=None)
    ram_types: str | None = Field(default=None)
    igp: bool | None = Field(default=None)

    tdp: int | None = Field(default=None)
    tdp_max: int | None = Field(default=None)

    cores: int | None = Field(default=None)
    threads: int | None = Field(default=None)


class RamSchema(BaseDbComponentSchema):
    type: str
    modules: int
    capacity: int
    speed: int

    cooling: bool | None = None
    colour: str | None = None
    lighting: bool | None = None


class GpuSchema(BaseDbComponentSchema):
    model_gpu: str

    memory_size: int
    memory_type: str

    monitors: int | None = None

    power_consumption: int
    additional_power: str | None = None

    # декор
    fans: int | None = None
    lighting: bool | None = None


class MotherboardSchema(BaseDbComponentSchema):
    socket: str
    form_factor: str
    ram_type: str
    ram_slots: int
    m2_count: int | None = None

    chipset: str

    lighting: bool | None = None
    vrm_heatsink: bool | None = None
    wifi: bool | None = None


class SsdSchema(BaseDbComponentSchema):
    form_factor: str

    volume: int | None = None
    read_speed: int | None = None
    write_speed: int | None = None

    controller: str | None = None
    interface_m2: str | None = None
    memory_type: str | None = None
    nvme: bool | None = None
    radiator: bool | None = None


class PowerSupplySchema(BaseDbComponentSchema):
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


if __name__ == "__main__":

    cpu = CpuSchema(
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
    ram = RamSchema(
        manufacturer="Corsair",
        model="Vengeance LPX",
        type="DDR5",
        modules=2,
        capacity=16,  # 16 GB total
        speed=3200,  # in MHz
    )
    gpu = GpuSchema(
        manufacturer="NVIDIA",
        model="GeForce RTX 3060",
        model_gpu="GA106",
        memory_size=12,  # in GB
        memory_type="GDDR6",
        power_consumption=170,  # in W
    )
    motherboard = MotherboardSchema(
        manufacturer="MSI",
        model="B550M PRO-VDH WIFI",
        socket="AM5",
        form_factor="mATX",
        ram_type="DDR4",
        ram_slots=4,
        m2_count=2,
        chipset="B550",
    )
    psu = PowerSupplySchema(
        manufacturer="be quiet!",
        model="Pure Power 12 M",
        form_factor="ATX",
        power=200,
        mb_and_cpu_powersupply="24+8 pin",
        plus_12v=200,  # in W
    )
