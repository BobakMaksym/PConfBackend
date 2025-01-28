from src.compatibilities import exceptions as ex
from src.compatibilities.rules import (
    CompatibilityRuleInterface,
    SocketCompatibilityRule,
)

from src.domain.base import Component
from src.domain.models import Cpu, Ram, Motherboard


class CompatibilityManager:
    def __init__(self):
        self.rules: list[CompatibilityRuleInterface] = []

    def add_rule(self, rule: CompatibilityRuleInterface):
        self.rules.append(rule)

    def check_compatibility(
        self, selected_components: list[Component], new_component: Component
    ) -> bool:
        """checks the compatibility of the new component with the list of selected
        `through all added rules`"""
        return all(
            rule.is_compatible(selected_components, new_component)
            for rule in self.rules
        )


compatibility_manager = CompatibilityManager()
compatibility_manager.add_rule(SocketCompatibilityRule())
# compatibility_manager.add_rule(RamTypeCompatibilityRule())
