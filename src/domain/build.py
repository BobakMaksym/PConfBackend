from dataclasses import dataclass

from src.domain.cpu import CPU
from src.domain.motherboard import MotherBoard
from src.domain.ram import RAM


@dataclass
class Build:
    cpu: CPU | None = None
    ram: RAM | None = None
    motherboard: MotherBoard | None = None

    # gpu: Optional[GPU] = None
    # psu: Optional[PSU] = None
