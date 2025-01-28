from dataclasses import dataclass

from src.domain.enums import ComponentType
from src.domain.models import Cpu
from src.domain.models import MotherBoard
from src.domain.models import Ram


@dataclass
class Build:
    cpu: Cpu | None = None
    ram: Ram | None = None
    motherboard: MotherBoard | None = None
