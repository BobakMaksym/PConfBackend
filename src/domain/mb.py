from dataclasses import dataclass
from src.domain.enums import ComponentType


@dataclass
class MotherBoard:
    _type = ComponentType.mother_board

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
