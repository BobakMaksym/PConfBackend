# rules_engine/core.py
from abc import ABC, abstractmethod
from typing import Iterable


class RuleInterface(ABC):
    """Базовий інтерфейс: повертає список помилок або порожній список."""

    @abstractmethod
    def validate(self, build) -> list[str]: ...
