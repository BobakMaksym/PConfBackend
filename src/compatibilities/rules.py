from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Annotated, Optional

from src.compatibilities import exceptions as e
from src.domain.base import Component
from src.domain.build import Build
from src.domain.enums import ComponentType


class CompatibilityRuleInterface(ABC):
    @abstractmethod
    def is_compatible(
        self,
        build: Build,
        new_component: Component,
        component_count: int = 1,
    ) -> bool:
        """checks if the new component is compatible with the already selected ones"""
        pass


class SocketCompatibilityRule(CompatibilityRuleInterface):
    def is_compatible(
        self,
        build: Build,
        new_component: Component | None = None,
    ) -> bool:
        """checks the socket compatibility of cpu and motherboard"""

        # якщо компонент НЕ підходящого типу, то немає сенсу перевіряти далі
        # тобто якщо ми перевіряємо cpu і motherboard, то не тре перевіряти збірку з ram
        if not new_component._type in (ComponentType.cpu, ComponentType.motherboard):
            return True

        """

        """

        # якщо немає нового, то тре перевірити додане
        if not new_component:

            cpu, mb = build.cpu, build.motherboard

            # якщо додані всі (cpu, motherboard)
            if all((cpu, mb)):
                cpu_sock, mb_sock = cpu.socket, mb.socket

                if cpu_sock == mb_sock:
                    return True
                else:
                    # тут потрібно буде генерувати помилки
                    errors = {}
                    return {"compatible": False, "errors": errors}
            # якщо потірбні компоенети не додані, значить помилок буде не може
            else:
                return True

        """

        """

        
        
        # додаю новий компонент до temp збірки
        temp_build = deepcopy(build)
        new_component_type = new_component._type
        setattr(temp_build, new_component_type, new_component)

        # items to check: CPU, Motherboard, RAM
        items_to_check = (ComponentType.cpu, ComponentType.motherboard)

        cpu = build.cpu
        motherboard = build.motherboard
        # якщо не всі ко
        if not all((cpu, motherboard)):
            return True

        """

        """

        build.motherboard.socket

        component_exception = {
            ComponentType.cpu: [
                "сокет cpu (LGA1700) не сумісний з сокетом плати (AM4)"
            ],
            ComponentType.motherboard: [
                "сокет плати (AM4) не сумісний з сокетом cpu (LGA1700)"
            ],
        }

        return {
            "compatible": bool,
        }


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


# class RamTypeOfCpuAndMotherboardCompRule(CompatibilityRuleInterface):
#     def is_compatible(
#         self, selected_components: list[Component], new_component: Component
#     ) -> bool:
#         """checks the RAM type compatibility of cpu and motherboard"""

#         component_types_to_check = {ComponentType.motherboard, ComponentType.cpu}

#         for component in selected_components:
#             if {component._type, new_component._type} == component_types_to_check:
#                 if component.ram_type != new_component.ram_type:
#                     raise e.RamTypeCompatibilityException(
#                         component.ram_type, new_component.ram_type
#                     )
#         return True
