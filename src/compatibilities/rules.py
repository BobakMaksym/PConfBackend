from abc import ABC, abstractmethod

from src.compatibilities import exceptions as e
from src.domain.base import Component
from src.domain.enums import ComponentType


class CompatibilityRuleInterface(ABC):
    @abstractmethod
    def is_compatible(
        self,
        selected_components: list[Component],
        new_component: Component,
    ) -> bool:
        """checks if the new component is compatible with the already selected ones"""
        pass


class SocketCompatibilityRule(CompatibilityRuleInterface):
    def is_compatible(
        self,
        selected_components: list[Component],
        new_component: Component,
    ) -> bool:
        """checks the socket compatibility of cpu and motherboard"""

        component_types_to_check = {ComponentType.motherboard, ComponentType.cpu}

        # ітеруємося по доданих компонентах, для знаходження потрібного, і порівняння з новим
        for component in selected_components:
            """перевірка поточного, доданого в збірку, компонента
            з новим компонентом, який хочемо додати, на правильність типів
            """
            if {component._type, new_component._type} == component_types_to_check:
                # перевірка сумісності по одному параметру
                if component.socket != new_component.socket:
                    raise e.SocketCompatibilityException(
                        component.socket, new_component.socket
                    )
        return True


class RamTypeOfCpuAndMotherboardCompRule(CompatibilityRuleInterface):
    def is_compatible(
        self, selected_components: list[Component], new_component: Component
    ) -> bool:
        """checks the RAM type compatibility of cpu and motherboard"""

        component_types_to_check = {ComponentType.motherboard, ComponentType.cpu}

        for component in selected_components:
            if {component._type, new_component._type} == component_types_to_check:
                if component.ram_type != new_component.ram_type:
                    raise e.RamTypeCompatibilityException(
                        component.ram_type, new_component.ram_type
                    )
        return True
