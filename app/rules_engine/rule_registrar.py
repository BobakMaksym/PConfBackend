from .core import Rule
from .standard_rules import (
    SocketCompatibility,
    RamTypeMatches,
    PsuPowerSufficiency,
)


_RULES: list[Rule] = []


def register(rule: Rule) -> None:
    """Додаємо правило у глобальний реєстр (можна й DI-контейнер)."""
    _RULES.append(rule)


def run(build) -> None:
    """Проганяємо всі правила; підійде й асинхронна версія."""
    errors: list[str] = []
    for rule in _RULES:
        errors.extend(rule.validate(build))

    print(f"\nCONFIGURATION ERRORS: {errors}\n")
    return errors


register(SocketCompatibility())
register(RamTypeMatches())
register(PsuPowerSufficiency())
