# rules_engine/core.py
from abc import ABC, abstractmethod
from typing import Iterable

from app.schemas.pc_config_schema import PcConfigSchema


class RuleInterface(ABC):
    """Базовий інтерфейс: повертає список помилок або порожній список."""

    @abstractmethod
    def validate(self, build: PcConfigSchema) -> list[str]: ...
