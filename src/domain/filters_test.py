from abc import ABC, abstractmethod


from dataclasses import dataclass
from typing import Optional


@dataclass
class Motherboard:
    socket: str
    memory_type: str


@dataclass
class CPU:
    socket: str


@dataclass
class RAM:
    memory_type: str


@dataclass
class Build:
    motherboard: Optional[Motherboard] = None
    cpu: Optional[CPU] = None
    ram: Optional[RAM] = None


class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, candidate) -> bool:
        """Перевіряє, чи відповідає кандидат критеріям."""
        pass

    @abstractmethod
    def as_filter(self) -> dict:
        """Повертає представлення умов у вигляді словника для запиту до БД."""
        pass


class AndSpecification(Specification):
    def __init__(self, *specs: Specification):
        self.specs = specs

    def is_satisfied_by(self, candidate) -> bool:
        return all(spec.is_satisfied_by(candidate) for spec in self.specs)

    def as_filter(self) -> dict:
        # Приклад: комбінуємо фільтри, простим об’єднанням словників.
        # В реальній системі, залежно від БД, це може бути більш складно.
        combined_filter = {}
        for spec in self.specs:
            combined_filter.update(spec.as_filter())
        return combined_filter


class SocketSpecification(Specification):
    def __init__(self, expected_socket: str):
        self.expected_socket = expected_socket

    def is_satisfied_by(self, candidate) -> bool:
        return getattr(candidate, "socket", None) == self.expected_socket

    def as_filter(self) -> dict:
        return {"socket": self.expected_socket}


class MemoryTypeSpecification(Specification):
    def __init__(self, expected_memory_type: str):
        self.expected_memory_type = expected_memory_type

    def is_satisfied_by(self, candidate) -> bool:
        return getattr(candidate, "memory_type", None) == self.expected_memory_type

    def as_filter(self) -> dict:
        return {"memory_type": self.expected_memory_type}


class ComponentFilterStrategy(ABC):
    @abstractmethod
    def generate(self, build) -> dict:
        """Генерує фільтр для пошуку сумісного компонента, виходячи з поточної конфігурації build."""
        pass


class CPUFilterStrategy(ComponentFilterStrategy):
    def generate(self, build) -> dict:
        specs = []
        # Припустимо, що для CPU важливі сокет і чіпсет материнської плати
        if build.motherboard:
            specs.append(SocketSpecification(build.motherboard.socket))
            # Якщо потрібна специфікація для чіпсету, її теж можна реалізувати аналогічно
            # specs.append(ChipsetSpecification(build.motherboard.chipset))
        if specs:
            combined = AndSpecification(*specs)
            return combined.as_filter()
        return {}


class RAMFilterStrategy(ComponentFilterStrategy):
    def generate(self, build) -> dict:
        specs = []
        # Для ОЗУ важливий тип пам'яті материнської плати
        if build.motherboard:
            specs.append(MemoryTypeSpecification(build.motherboard.memory_type))
        if specs:
            combined = AndSpecification(*specs)
            return combined.as_filter()
        return {}


class FilterStrategyRegistry:
    _registry = {}

    @classmethod
    def register(cls, component_type: str, strategy: ComponentFilterStrategy):
        cls._registry[component_type] = strategy

    @classmethod
    def get_strategy(cls, component_type: str) -> ComponentFilterStrategy:
        strategy = cls._registry.get(component_type)
        if not strategy:
            raise ValueError(f"Strategy for {component_type} is not registered.")
        return strategy


# Реєструємо існуючі стратегії
FilterStrategyRegistry.register("CPU", CPUFilterStrategy())
FilterStrategyRegistry.register("RAM", RAMFilterStrategy())


def get_compatible_filters(build, component_type: str) -> dict:
    strategy = FilterStrategyRegistry.get_strategy(component_type)
    return strategy.generate(build)


# Приклад створення материнської плати та інших компонентів
motherboard = Motherboard(socket="AM4", memory_type="DDR4")
cpu = CPU(socket="AM4")
ram = RAM(memory_type="DDR4")

# Формуємо поточну збірку
build = Build(motherboard=motherboard, cpu=cpu, ram=ram)


# Приклад використання:
# build – це об’єкт вашої конфігурації (як приклад, dataclass Build, який містить посилання на CPU, Motherboard, RAM тощо)
filters_for_ram = get_compatible_filters(build, "RAM")
print(filters_for_ram)  # Наприклад, {'memory_type': 'DDR4'}


# Генеруємо фільтр для CPU
filters_for_cpu = get_compatible_filters(build, "CPU")
print("CPU Filters:", filters_for_cpu)  # Очікуваний результат: {'socket': 'AM4'}

# Генеруємо фільтр для RAM
filters_for_ram = get_compatible_filters(build, "RAM")
print("RAM Filters:", filters_for_ram)  # Очікуваний результат: {'memory_type': 'DDR4'}
