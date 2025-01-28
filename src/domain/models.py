from dataclasses import dataclass
from src.domain.enums import ComponentType


@dataclass
class Cpu:
    _type = ComponentType.cpu

    art: str
    manufacturer: str
    model: str
    series: str

    socket: str
    tdp: int
    ram_type: str
    max_ram: int

    # cores: int
    # threads: int

    # other: dict = field(default_factory=dict)


@dataclass
class Ram:
    _type = ComponentType.ram

    art: str
    model: str
    manufacturer: str
    series: str  # Trident Z/Sniper X

    ram_type: str
    speed: int
    kit: int
    kit_total_capacity: int


@dataclass
class MotherBoard:
    _type = ComponentType.motherboard

    # art: str | None = None
    model: str
    manufacturer: str
    series: str  # Aorus/Gaming/Tuf

    platform: str  # Intel/AMD
    socket: str
    ram_type: str
    max_ram: int

    chipset: str
    # form_factor: str
