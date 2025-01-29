from dataclasses import dataclass, asdict
from pprint import pprint

from src.compatibilities import exceptions as ex
from src.compatibilities.rules import CompatibilityRuleInterface, rules

from src.domain.models import Component
from src.domain.models import Build, CompatibilityErrors, ErrorsInfo
from src.domain.models import Cpu, Ram, Motherboard


class CompatibilityManager:
    def __init__(self):
        self.rules: list[CompatibilityRuleInterface] = []

    def add_rule(self, rule: CompatibilityRuleInterface):
        self.rules.append(rule)

    def check_compatibility(self, build: Build):
        """checks the compatibility of the new component with the list of selected
        `through all added rules`"""

        # проганяє збірку через всі правила;
        # збирає error-и з правил в один словник;

        # можливо додати щось типу статусу збірки
        # (збірка коректна, збірка завершена на 60%)

        # errors: dict[str, list[str]] = {}

        for rule in self.rules:
            res = rule.check(build)

            # print(f"{rule.__class__.__name__}  \t{res.compatible}")

            for key, val in res.errors.items():
                component_errors_info: ErrorsInfo = getattr(build.errors, key)

                component_errors_info.list_.append(val)
                component_errors_info.count += 1


compatibility_manager = CompatibilityManager()
for rule in rules:
    compatibility_manager.add_rule(rule())
