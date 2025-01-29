from src.domain.models import Component
from src.domain.models import Build
from src.domain.models import Cpu
from src.domain.models import Motherboard

from src.compatibilities.manager import CompatibilityManager, compatibility_manager


class Configurator:
    def __init__(
        self,
        components: list[Component],
        compatibility_manager: CompatibilityManager,
    ):
        self.build = Build()

        self.selected_components: list[Component] = []
        self.compatibility_manager = compatibility_manager

    def add_components(self, new_component: Component):
        if self.compatibility_manager.check_compatibility(
            self.selected_components,
            new_component,
        ):
            self.selected_components.append(new_component)
            return True
        return False

    def get_selected_components(self) -> list[Component]:
        return self.selected_components


# amd_am5_ddr5 = cpu_db[0]
# aorus_amd_am5 = motherboard_db[4]


# res = configurator.add_components(amd_am5_ddr5)
# print(res)
# res = configurator.add_components(aorus_amd_am5)
# print(res)
