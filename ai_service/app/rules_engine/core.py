# rules_engine/core.py
from abc import ABC, abstractmethod
from typing import Iterable, List


class BuildValidationError(ValueError):
    """Збирає всі помилки сумісності."""

    def __init__(self, errors: List[str]) -> None:
        super().__init__("\n".join(errors))
        self.errors = errors


class Rule(ABC):
    """Базовий інтерфейс: повертає список помилок або порожній список."""

    @abstractmethod
    def validate(self, build) -> List[str]: ...
