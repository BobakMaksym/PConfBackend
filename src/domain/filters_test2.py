from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum
from abc import ABC, abstractmethod

# =======================
# 1. Моделі компонентів
# =======================


@dataclass
class Cpu:
    manufacturer: str = None
    socket: str = None
    codename: str = None
    ram_types: List[str] = None  # Наприклад: ["DDR4"]


@dataclass
class Ram:
    manufacturer: Optional[str] = None
    ram_type: Optional[str] = None
    memory_capacity: Optional[int] = None  # У ГБ
    memory_modules: Optional[int] = None


@dataclass
class Gpu:
    power: Optional[int] = None  # Споживана потужність, наприклад, у ватах


class MbTypeEnum(str, Enum):
    atx = "ATX"
    mini_atx = "mini ATX"


@dataclass
class Motherboard:
    manufacturer: str = None
    platform: str = None  # Наприклад, "Intel" або "AMD"
    socket: str = None
    chipset: str = None
    cpu_codenames: List[str] = None  # Наприклад: ["Ryzen 5 3600", "Ryzen 7 3700X"]
    ram_type: str = None
    motherboard_type: MbTypeEnum = MbTypeEnum.atx


# =======================
# 2. Модель збірки (Build)
# =======================


@dataclass
class Build:
    cpu: Optional[Cpu] = None
    motherboard: Optional[Motherboard] = None
    ram: Optional[Ram] = None
    gpu: Optional[Gpu] = None


# =======================================
# 3. Патерн Specification (абстракція умов)
# =======================================


class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, candidate) -> bool:
        """Перевіряє, чи відповідає кандидат умовам специфікації."""
        pass

    @abstractmethod
    def as_filter(self) -> Dict[str, Any]:
        """
        Повертає представлення умов у вигляді словника,
        який можна використати в запитах до БД.
        """
        pass


class AndSpecification(Specification):
    """Комбінує декілька специфікацій за логікою 'І'."""

    def __init__(self, *specs: Specification):
        self.specs = specs

    def is_satisfied_by(self, candidate) -> bool:
        return all(spec.is_satisfied_by(candidate) for spec in self.specs)

    def as_filter(self) -> Dict[str, Any]:
        combined = {}
        for spec in self.specs:
            combined.update(spec.as_filter())
        return combined


# Специфікація для перевірки сокету
class SocketSpecification(Specification):
    def __init__(self, expected_socket: str):
        self.expected_socket = expected_socket

    def is_satisfied_by(self, candidate) -> bool:
        return getattr(candidate, "socket", None) == self.expected_socket

    def as_filter(self) -> Dict[str, Any]:
        return {"socket": self.expected_socket}


# Специфікація для перевірки підтримуваного типу оперативної пам'яті для CPU.
class SupportedRamTypeSpecification(Specification):
    """
    Перевіряє, чи міститься в списку підтримуваних типів пам'яті
    у CPU потрібний тип (наприклад, "DDR4").
    """

    def __init__(self, expected_ram_type: str):
        self.expected_ram_type = expected_ram_type

    def is_satisfied_by(self, candidate) -> bool:
        if candidate.ram_types is None:
            return False
        return self.expected_ram_type in candidate.ram_types

    def as_filter(self) -> Dict[str, Any]:
        # Припускаємо, що система запитів підтримує пошук за списками.
        return {"ram_types__contains": self.expected_ram_type}


# Специфікація для перевірки типу пам'яті для RAM.
class RamTypeSpecification(Specification):
    def __init__(self, expected_ram_type: str):
        self.expected_ram_type = expected_ram_type

    def is_satisfied_by(self, candidate) -> bool:
        return getattr(candidate, "ram_type", None) == self.expected_ram_type

    def as_filter(self) -> Dict[str, Any]:
        return {"ram_type": self.expected_ram_type}


# Для Motherboard: перевірка, чи підтримує материнка певний код назви процесора.
class CpuCodenameSpecification(Specification):
    def __init__(self, expected_cpu_codename: str):
        self.expected_cpu_codename = expected_cpu_codename

    def is_satisfied_by(self, candidate) -> bool:
        if candidate.cpu_codenames is None:
            return False
        return self.expected_cpu_codename in candidate.cpu_codenames

    def as_filter(self) -> Dict[str, Any]:
        return {"cpu_codenames__contains": self.expected_cpu_codename}


# Для Motherboard: перевірка сокету материнської плати.
class MbSocketSpecification(Specification):
    def __init__(self, expected_socket: str):
        self.expected_socket = expected_socket

    def is_satisfied_by(self, candidate) -> bool:
        return getattr(candidate, "socket", None) == self.expected_socket

    def as_filter(self) -> Dict[str, Any]:
        return {"socket": self.expected_socket}


# Для Motherboard: перевірка типу пам'яті материнської плати.
class MotherboardRamTypeSpecification(Specification):
    def __init__(self, expected_ram_type: str):
        self.expected_ram_type = expected_ram_type

    def is_satisfied_by(self, candidate) -> bool:
        return getattr(candidate, "ram_type", None) == self.expected_ram_type

    def as_filter(self) -> Dict[str, Any]:
        return {"ram_type": self.expected_ram_type}


# ==================================================
# 4. Патерн Strategy для генерації фільтрів для компонентів
# ==================================================


class ComponentFilterStrategy(ABC):
    @abstractmethod
    def generate(self, build: Build) -> Dict[str, Any]:
        """Генерує фільтр для пошуку сумісного компонента."""
        pass


class CPUFilterStrategy(ComponentFilterStrategy):
    def generate(self, build: Build) -> Dict[str, Any]:
        """
        Для CPU перевіряємо:
          - Чи співпадає сокет з материнською платою.
          - Чи підтримує CPU тип пам'яті, що використовується материнською платою.
        """
        specs = []
        if build.motherboard:
            specs.append(SocketSpecification(build.motherboard.socket))
            if build.motherboard.ram_type:
                specs.append(SupportedRamTypeSpecification(build.motherboard.ram_type))
        if specs:
            combined_spec = AndSpecification(*specs)
            return combined_spec.as_filter()
        return {}


class RAMFilterStrategy(ComponentFilterStrategy):
    def generate(self, build: Build) -> Dict[str, Any]:
        """
        Для RAM перевіряємо:
          - Чи співпадає тип пам'яті з тим, що підтримує материнська плата.
        """
        if build.motherboard:
            if build.motherboard.ram_type:
                spec = RamTypeSpecification(build.motherboard.ram_type)
                return spec.as_filter()
        return {}


class MotherboardFilterStrategy(ComponentFilterStrategy):
    def generate(self, build: Build) -> Dict[str, Any]:
        """
        Для материнської плати перевіряємо:
          - Чи співпадає сокет з процесором.
          - Чи підтримує материнська плата дану кодову назву процесора.
          - Чи співпадає тип пам'яті (для спрощення, беремо перший підтримуваний тип з CPU).
        """
        specs = []
        if build.cpu:
            specs.append(MbSocketSpecification(build.cpu.socket))
            if build.cpu.codename:
                specs.append(CpuCodenameSpecification(build.cpu.codename))
            # Припустимо, що CPU підтримує хоча б один тип пам'яті.
            if build.cpu.ram_types and len(build.cpu.ram_types) > 0:
                specs.append(MotherboardRamTypeSpecification(build.cpu.ram_types[0]))
        if specs:
            combined_spec = AndSpecification(*specs)
            return combined_spec.as_filter()
        return {}


class GPUFilterStrategy(ComponentFilterStrategy):
    def generate(self, build: Build) -> Dict[str, Any]:
        """
        Для GPU у цьому прикладі задаємо простий фільтр за потужністю:
          Якщо у збірці вже є GPU з певною потужністю,
          будемо шукати моделі, потужність яких знаходиться в діапазоні ±50 ват.
        """
        if build.gpu and build.gpu.power is not None:
            lower_bound = build.gpu.power - 50
            upper_bound = build.gpu.power + 50
            return {"power__gte": lower_bound, "power__lte": upper_bound}
        return {}


# ==================================================
# 5. Реєстр стратегій для отримання потрібної логіки фільтрації
# ==================================================


class FilterStrategyRegistry:
    _registry: Dict[str, ComponentFilterStrategy] = {}

    @classmethod
    def register(cls, component_type: str, strategy: ComponentFilterStrategy):
        cls._registry[component_type] = strategy

    @classmethod
    def get_strategy(cls, component_type: str) -> ComponentFilterStrategy:
        if component_type not in cls._registry:
            raise ValueError(
                f"No strategy registered for component type: {component_type}"
            )
        return cls._registry[component_type]


# def get_compatible_filters(build: Build, component_type: str) -> Dict[str, Any]:
#     """
#     Отримуємо фільтр сумісності для заданого типу компоненту.
#     """
#     strategy = FilterStrategyRegistry.get_strategy(component_type)
#     return strategy.generate(build)


# ==================================================
# 6. Приклади використання з поясненнями
# ==================================================

# Приклад 1: Повна збірка з усіма компонентами
cpu_example = Cpu(
    manufacturer="AMD",
    socket="AM4",
    codename="Ryzen 5 3600",
    ram_types=["DDR4", "DDR5"],
)
motherboard_example = Motherboard(
    manufacturer="ASUS",
    platform="AMD",
    socket="AM4",
    chipset="B450",
    cpu_codenames=["Ryzen 5 3600", "Ryzen 7 3700X"],
    ram_type="DDR4",
    motherboard_type=MbTypeEnum.atx,
)
ram_example = Ram(
    manufacturer="Corsair", ram_type="DDR4", memory_capacity=16, memory_modules=2
)
gpu_example = Gpu(power=150)
build_example = Build(
    cpu=cpu_example, motherboard=motherboard_example, ram=ram_example, gpu=gpu_example
)


# Реєструємо стратегії для кожного типу компонентів
FilterStrategyRegistry.register("CPU", CPUFilterStrategy())
FilterStrategyRegistry.register("RAM", RAMFilterStrategy())
FilterStrategyRegistry.register("Motherboard", MotherboardFilterStrategy())
FilterStrategyRegistry.register("GPU", GPUFilterStrategy())


# Генеруємо фільтри для різних компонентів

# Фільтр для CPU: шукаємо процесори, у яких сокет = "AM4" та підтримується "DDR4"
strategy = FilterStrategyRegistry.get_strategy("CPU")
cpu_filters = strategy.generate(build_example)
print("Filters for CPU:", cpu_filters)
# Приблизний очікуваний результат: {'socket': 'AM4', 'ram_types__contains': 'DDR4'}

# Фільтр для RAM: шукаємо пам'ять з типом "DDR4"
strategy = FilterStrategyRegistry.get_strategy("RAM")
ram_filters = strategy.generate(build_example)
print("Filters for RAM:", ram_filters)
# Очікувано: {'ram_type': 'DDR4'}

# Фільтр для материнської плати:
# має мати сокет "AM4", підтримувати кодову назву "Ryzen 5 3600" та тип пам'яті "DDR4"
strategy = FilterStrategyRegistry.get_strategy("Motherboard")
mb_filters = strategy.generate(build_example)
print("Filters for Motherboard:", mb_filters)
# Очікувано: {'socket': 'AM4', 'cpu_codenames__contains': 'Ryzen 5 3600', 'ram_type': 'DDR4'}

# Фільтр для GPU: шукаємо відеокарти з потужністю в діапазоні 100-200 ват (150±50)
strategy = FilterStrategyRegistry.get_strategy("GPU")
gpu_filters = strategy.generate(build_example)
print("Filters for GPU:", gpu_filters)
# Очікувано: {'power__gte': 100, 'power__lte': 200}


# Приклад 2: Збірка без материнської плати
# Якщо немає материнської плати, деякі фільтри не можуть бути сформовані
build_incomplete = Build(cpu=cpu_example, ram=ram_example, gpu=gpu_example)

strategy = FilterStrategyRegistry.get_strategy("CPU")
cpu_filters_incomplete = strategy.generate(build_incomplete)

print("Incomplete build - CPU Filters:", cpu_filters_incomplete)
# Очікувано: {} - бо для CPU немає інформації з материнської плати для порівняння.
