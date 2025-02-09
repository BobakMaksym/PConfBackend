from abc import ABC
from dataclasses import dataclass, field, asdict
from enum import Enum


class ComponentType(str, Enum):
    cpu = "cpu"
    gpu = "gpu"
    ram = "ram"
    psu = "psu"
    motherboard = "motherboard"


class Component(ABC):
    _type: ComponentType


# #########################################################


@dataclass
class PowerConnector:
    """
    Описує фізичний конектор (кабель) з БЖ.
    Наприклад: "6+2" для PCIe або "20+4" для ATX.
    """

    type: str  # наприклад, "ATX", "EPS", "PCIe"
    pins: tuple[int, ...]  # кортеж із секціями, наприклад (6, 2) або (20, 4)


@dataclass
class ComponentPowerSlots:
    """
    Описує слот(и) живлення на компоненті (материнська плата, CPU, GPU).
    Наприклад, для відеокарти: [8, 6] – один 8-піновий та один 6-піновий роз'єм.
    """

    type: str  # тип слоту, наприклад "PCIe", "EPS", "ATX"
    slots: list[int]  # список кількостей пінів, які потрібні


@dataclass
class PSUCable:
    """
    Модель кабелю з БЖ для алгоритму розподілу.
    - type: тип кабелю ("ATX", "EPS", "PCIe")
    - sections: список секцій (кількість пінів у кожній секції)
    - splitable: якщо кабель має більше однієї секції, і їх можна роз'єднати (наприклад, "6+2" або "4+4").
      Якщо кабель є окремим роз'ємом (тобто кортеж з одним числом), splitable=False.
    - available: список доступних секцій (для розподілу). Якщо кабель не роздільний, це один елемент,
      що дорівнює сумі секцій.
    """

    type: str
    sections: list[int]
    splitable: bool = field(init=False)
    available: list[int] = field(init=False)

    def __post_init__(self):
        # Якщо більше однієї секції – кабель можна розділити
        self.splitable = len(self.sections) > 1
        if self.splitable:
            # Спочатку усі секції доступні окремо
            self.available = self.sections.copy()
        else:
            # Не роздільний – єдиний «цілий» роз'єм
            self.available = [self.sections[0]]

    def clone(self) -> "PSUCable":
        """Повертає копію кабелю з його поточним станом available."""
        new = PSUCable(self.type, self.sections.copy())
        new.splitable = self.splitable
        new.available = self.available.copy()
        return new


@dataclass
class PowerSupply:
    """
    Описує БЖ і його вихідні кабелі.
    """

    power: int = None
    connectors: list[PowerConnector] = None


# #########################################################


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
    tdp_max: int = None
    ram_types: list[str] = None
    max_ram: int = None
    _type = ComponentType.cpu.value

    def __post_init__(self):
        if not self.tdp_max:
            self.tdp_max = self.tdp


@dataclass
class Ram:
    art: str | None = None
    model: str | None = None
    manufacturer: str | None = None
    series: str | None = None

    ram_type: str | None = None
    speed: int | None = None

    memory_capacity: int | None = None
    memory_modules: int | None = None
    count: int = 0  # number of modules added to the assembly by the user

    _type = ComponentType.ram.value


@dataclass
class Gpu:
    power: int | None = None
    power_slots: ComponentPowerSlots | None = None
    count: int = 0  # number of gpu added to the assembly by the user


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

    power_atx_slots: ComponentPowerSlots = None
    power_eps_slots: ComponentPowerSlots = None

    _type = ComponentType.motherboard.value


@dataclass
class SsdM2:
    count: int = 0  # number of ssd added to the assembly by the user


@dataclass
class Hdd:
    count: int = 0  # number of hdd added to the assembly by the user


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
    gpu: Gpu | None = None
    psu: PowerSupply | None = None

    errors: CompatibilityErrors = field(default_factory=CompatibilityErrors)


if __name__ == "__main__":
    cpu1 = Cpu(manufacturer="AMD")

    build1 = Build(cpu=cpu1)

    print(build1.cpu.manufacturer)
    print()
    print(build1.errors.cpu.list_)
    print()
    print(asdict(build1.errors))
