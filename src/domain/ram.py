from dataclasses import dataclass

from src.domain.enums import ComponentType


@dataclass
class RAM:
    _type = ComponentType.ram

    art: str
    model: str
    manufacturer: str
    series: str  # Trident Z/Sniper X

    ram_type: str
    speed: int
    kit: int
    kit_total_capacity: int
