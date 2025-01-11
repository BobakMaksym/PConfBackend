from src.domain.cpu import CPU, cpu_db
from src.domain.motherboard import MotherBoard, motherboard_db

from src.compatibilities.manager import CompatibilityManager, compatibility_manager


class PCConfigurator:
    def __init__(self, compatibility_manager: CompatibilityManager):
        self.selected_components: list[object] = []
        self.compatibility_manager = compatibility_manager

    def add_components(self, new_component):
        if self.compatibility_manager.check_compatibility(
            self.selected_components,
            new_component,
        ):
            self.selected_components.append(new_component)
            return True
        return False

    def get_selected_components(self):
        return self.selected_components


configurator = PCConfigurator(compatibility_manager)


amd_am5_ddr5 = cpu_db[0]
aorus_amd_am5 = motherboard_db[4]


res = configurator.add_components(amd_am5_ddr5)
print(res)
res = configurator.add_components(aorus_amd_am5)
print(res)


# res = compatibility_manager.check_compatibility([amd_am5_ddr5], aorus_amd_am5)
# print(res)

# # print(amd_am5_ddr5, mb)
