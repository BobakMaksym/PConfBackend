from app.rules_engine.core import RuleInterface


class CompatibilityManager:
    def __init__(self):
        self.rules: list[RuleInterface] = []

    def add_rule(self, rule: RuleInterface):
        self.rules.append(rule)

    def check_compatibility(self, build):
        """checks the compatibility of the new component with the list of selected
        `through all added rules`"""

        errors: list[str] = []
        for rule in self.rules:
            errors.extend(rule.validate(build))

        print(f"\nCONFIGURATION ERRORS: {errors}\n")
        return errors


rule_manager = CompatibilityManager()


# _RULES: list[Rule] = []


# def register(rule: Rule) -> None:
#     """Додаємо правило у глобальний реєстр (можна й DI-контейнер)."""
#     _RULES.append(rule)


# def run(build) -> None:
#     """Проганяємо всі правила; підійде й асинхронна версія."""
#     errors: list[str] = []
#     for rule in _RULES:
#         errors.extend(rule.validate(build))

#     print(f"\nCONFIGURATION ERRORS: {errors}\n")
#     return errors


# register(SocketCompatibility())
# register(RamTypeMatches())
# register(PsuPowerSufficiency())
