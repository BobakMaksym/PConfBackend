from abc import ABC
from dataclasses import dataclass, field, asdict
from enum import Enum


class ComponentType(str, Enum):
    cpu = "cpu"
    gpu = "gpu"
    ram = "ram"
    pcu = "pcu"
    motherboard = "motherboard"


class Component(ABC):
    _type: ComponentType


@dataclass
class Cpu:
    art: str = None
    manufacturer: str = None
    model: str = None
    series: str = None

    socket: str = None
    # core name / codename / family
    codename: str = None  # Raptor Lake | Picasso
    tdp: int = None
    ram_type: str = None
    max_ram: int = None
    _type = ComponentType.cpu.value


@dataclass
class Ram:
    art: str | None = None
    model: str | None = None
    manufacturer: str | None = None
    series: str | None = None

    ram_type: str | None = None
    speed: int | None = None
    kit: int | None = None
    kit_total_capacity: int | None = None

    _type = ComponentType.ram.value


@dataclass
class Motherboard:
    model: str = None
    manufacturer: str = None
    series: str = None  # Aorus/Gaming/Tuf

    platform: str = None  # Intel/AMD
    socket: str = None
    chipset: str = None
    cpu_codenames: list[str] = None  # [Raptor Lake, Alder Lake]
    ram_type: str = None
    max_ram: int = None
    _type = ComponentType.motherboard.value


# #########################################################


@dataclass
class ErrorsInfo:
    list_: list[str] = field(default_factory=list)
    count: int = 0


@dataclass
class CompatibilityErrors:
    cpu: ErrorsInfo = field(default_factory=ErrorsInfo)
    ram: ErrorsInfo = field(default_factory=ErrorsInfo)
    motherboard: ErrorsInfo = field(default_factory=ErrorsInfo)


@dataclass
class Build:
    cpu: Cpu | None = None
    ram: Ram | None = None
    motherboard: Motherboard | None = None

    errors: CompatibilityErrors = field(default_factory=CompatibilityErrors)


if __name__ == "__main__":
    cpu1 = Cpu(manufacturer="AMD")

    build1 = Build(cpu=cpu1)

    print(build1.cpu.manufacturer)
    print()
    print(build1.errors.cpu.list_)
    print()
    print(asdict(build1.errors))
