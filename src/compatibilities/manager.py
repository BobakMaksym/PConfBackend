from src.domain.cpu import CPU, cpu_db
from src.domain.motherboard import MotherBoard, motherboard_db
from src.domain.ram import RAM, ram_db

from src.compatibilities import exceptions as ex
from src.compatibilities.rules import (
    CompatibilityRuleInterface,
    SocketCompatibilityRule,
)

# , RamTypeCompatibilityRule


class CompatibilityManager:
    def __init__(self):
        self.rules: list[CompatibilityRuleInterface] = []

    def add_rule(self, rule: CompatibilityRuleInterface):
        self.rules.append(rule)

    def check_compatibility(
        self, selected_components: list[object], new_component: object
    ) -> bool:
        return all(
            rule.is_compatible(selected_components, new_component)
            for rule in self.rules
        )


compatibility_manager = CompatibilityManager()
compatibility_manager.add_rule(SocketCompatibilityRule())
# compatibility_manager.add_rule(RamTypeCompatibilityRule())
