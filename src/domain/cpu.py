from dataclasses import dataclass

from src.domain.enums import ComponentType


@dataclass
class CPU:
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
