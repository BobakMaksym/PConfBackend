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


_RULES: list[Rule] = []


def register(rule: Rule) -> None:
    """Додаємо правило у глобальний реєстр (можна й DI-контейнер)."""
    _RULES.append(rule)


def run(build) -> None:
    """Проганяємо всі правила; підійде й асинхронна версія."""
    errors: list[str] = []
    for rule in _RULES:
        errors.extend(rule.validate(build))
    # if errors:
    #     raise BuildValidationError(errors)

    # for err in errors:
    print(errors)
