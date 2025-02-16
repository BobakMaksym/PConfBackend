from abc import ABC, abstractmethod
from typing import Any

"""
якщо вибираю mb

вибір:
- повернути сумісні mb
- повернути не сумісні mb

if cpu: ...
if ram: ...

в умовах буде генерація фільтрів
"""

from src.domain.models import Cpu, Motherboard, Ram, Build


def set_filter(
    _filters: dict,
    param_in_component: Any,
    param_target: str,
):
    if param_in_component:
        _filters[param_target] = param_in_component


class ComponentStrategy(ABC):
    def __init__(self):
        self._filters = {}

    @abstractmethod
    def execute(self, build: Build) -> dict:
        pass


class CpuStrategy(ComponentStrategy):
    def execute(self, build: Build):

        ram = build.ram
        if ram:
            set_filter(self._filters, ram.ram_type, "ram_types")

        mb = build.motherboard
        if mb:
            set_filter(self._filters, mb.platform, "manufacturer")
            set_filter(self._filters, mb.socket, "socket")
            set_filter(self._filters, mb.cpu_codenames, "codename")
            set_filter(self._filters, mb.ram_type, "ram_types")

        return self._filters


class MotherboardStrategy(ComponentStrategy):
    def execute(self, build: Build):
        """
        cpu може працювати з різними типами ram
        ram - тільки з одним
        mb - те ж
        """

        ram = build.ram
        if ram:
            set_filter(self._filters, ram.ram_type, "ram_type")

        case_ = build.case_
        if case_:
            set_filter(self._filters, case_.motherboard_type, "motherboard_type")

        cpu = build.cpu
        if cpu:
            set_filter(self._filters, cpu.manufacturer, "platform")
            set_filter(self._filters, cpu.socket, "socket")
            set_filter(self._filters, cpu.codename, "cpu_codenames__in")
            set_filter(self._filters, cpu.ram_types, "ram_type__in")

        return self._filters


class RamStrategy(ComponentStrategy):
    def execute(self, build: Build):
        """
        cpu може працювати з різними типами ram
        ram - тільки з одним
        mb - те ж
        """

        cpu = build.cpu
        if cpu:
            set_filter(self._filters, cpu.ram_types, "ram_type__in")

        mb = build.motherboard
        if mb:
            set_filter(self._filters, mb.ram_type, "ram_type")

        return self._filters


class StrategyRegistry:
    # _strategy: ComponentStrategy

    def __init__(self, build: Build, strategy: ComponentStrategy):
        self.build = build
        self._strategy = strategy

    def set_strategy(self, strategy: ComponentStrategy):
        self._strategy = strategy

    def generate_filters(self):
        filters = self._strategy.execute(self.build)
        return filters
