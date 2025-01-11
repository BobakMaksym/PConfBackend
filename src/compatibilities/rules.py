from abc import ABC, abstractmethod

from src.compatibilities import exceptions as ex
from src.domain.enums import ComponentType


class CompatibilityRuleInterface(ABC):
    @abstractmethod
    def is_compatible(
        self,
        selected_components: list[object],
        new_component: object,
    ) -> bool:
        """checks if the new component is compatible with the already selected ones"""
        pass


class SocketCompatibilityRule(CompatibilityRuleInterface):
    def is_compatible(
        self,
        selected_components: list[object],
        new_component: object,
    ) -> bool:
        """checks the compatibility of the cpu socket and the motherboard"""

        for component in selected_components:
            if (
                component._type == ComponentType.cpu
                and new_component._type == ComponentType.motherboard
            ):
                if component.socket == new_component.socket:
                    return True
                raise ex.SocketCompatibilityException(
                    component.socket, new_component.socket
                )
            if (
                component._type == ComponentType.motherboard
                and new_component._type == ComponentType.cpu
            ):
                if component.socket == new_component.socket:
                    return True
                raise ex.SocketCompatibilityException(
                    component.socket, new_component.socket
                )
        return True


# class RamTypeCompatibilityRule(CompatibilityRuleInterface):
#     def is_compatible(
#         self, selected_components: list[object], new_component: object
#     ) -> bool:
#         for component in selected_components:
#             if isinstance(component, MotherBoard) and isinstance(new_component, RAM):
#                 return component.ram_type == new_component.ram_type
#             if isinstance(component, RAM) and isinstance(new_component, MotherBoard):
#                 return component.ram_type == new_component.ram_type
#         return True
