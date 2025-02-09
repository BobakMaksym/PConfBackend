from dataclasses import dataclass
from pprint import pprint
from unittest import TestCase

from src.compatibilities.rules import (
    CompatibilityRuleInterface,
    # platform
    PlatformCpuAndMotherboardCompRule,
    # socket
    SocketCpuAndMotherboardCompRule,
    # mb
    MotherboardChipsetSupportsCpuRule,
    # ram
    RamTypeInCpuAndMotherboardCompRule,
    RamTypeInCpuAndRamCompRule,
    RamTypeInMotherboardAndRamCompRule,
    # psu
    MotherboardPowerCompRule,
    MotherboardCpuPowerCompRule,
    GpuPowerCompRule,
    PsuWattageRule,
    rules as compatibility_rules,
)
from src.domain.models import Component
from src.domain.models import Build
from src.domain.models import ComponentType, Cpu, Motherboard, Ram, Gpu
from src.domain.models import PowerSupply, PowerConnector, ComponentPowerSlots


class CommonMixin:

    def setUp(self):
        pass

    def base(
        self,
        first: Component,
        second: Component,
        rule: CompatibilityRuleInterface,
        msg: str = "",
        exp_compatibility: bool = True,
    ):
        build = Build()
        first_t = first.__class__.__name__.lower()
        second_t = second.__class__.__name__.lower()

        setattr(build, first_t, first)
        setattr(build, second_t, second)

        compatible = rule.check(build).compatible

        if exp_compatibility:
            self.assertTrue(compatible, f"{msg} must be compatible")
        else:
            self.assertFalse(compatible, f"{msg} must be incompatible")


class TestCpuCompatibilitiesRules(CommonMixin, TestCase):

    def test_add_cpu_in_empty_build(self):
        """перевіряю роботу правила при додаванні cpu в пусту збірку"""

        rule = SocketCpuAndMotherboardCompRule()
        build = Build(cpu=Cpu("Intel"))

        compatible = rule.check(build).compatible

        self.assertTrue(compatible, "component was not added to an empty build")

    # Test `platform` compatibility

    def test_cpu_and_mb_platform_compatibility_is_true(self):
        """check platform of cpu & mb compatibility"""

        first, second = "AMD", "AMD"

        self.base(
            Cpu(manufacturer=first),
            Motherboard(platform=second),
            PlatformCpuAndMotherboardCompRule(),
            f"platform in `cpu` ({first}) and `motherboard` ({second})",
        )

    def test_cpu_and_mb_platform_compatibility_is_false(self):
        """check platform of cpu & mb incompatibility"""

        first, second = "AMD", "Intel"

        self.base(
            Cpu(manufacturer=first),
            Motherboard(platform=second),
            PlatformCpuAndMotherboardCompRule(),
            f"platform in `cpu` ({first}) and `motherboard` ({second})",
            exp_compatibility=False,
        )

    # Test `socket` compatibility

    def test_cpu_and_mb_socket_compatibility_is_true(self):
        """перевірка сокетів cpu і mb на сумісніть"""

        value = "AM4"

        self.base(
            Cpu(socket=value),
            Motherboard(socket=value),
            SocketCpuAndMotherboardCompRule(),
            f"socket in `cpu` ({value}) and `motherboard` ({value})",
        )

    def test_cpu_and_mb_socket_compatibility_is_false(self):
        """перевірка сокетів cpu і mb на несумісніть"""

        first, second = "AM4", "LGA1200"

        self.base(
            Cpu(socket=first),
            Motherboard(socket=second),
            SocketCpuAndMotherboardCompRule(),
            f"socket in `cpu` ({first}) and `motherboard` ({second})",
            exp_compatibility=False,
        )

    # Test of supported processors, chipsets

    def test_mb_supports_cpu_is_true(self):
        codename = "Rocket Lake"
        codenames = ("Rocket Lake", "Comet Lake")

        self.base(
            Cpu(codename=codename),
            Motherboard(cpu_codenames=codenames),
            MotherboardChipsetSupportsCpuRule(),
            f"`motherboard` ({codenames}) and `cpu` ({codename})",
        )

    def test_mb_supports_cpu_is_false(self):
        codename = "Picasso"
        codenames = ("Rocket Lake", "Comet Lake")

        self.base(
            Cpu(codename=codename),
            Motherboard(cpu_codenames=codenames),
            MotherboardChipsetSupportsCpuRule(),
            f"`motherboard` ({codenames}) and `cpu` ({codename})",
            exp_compatibility=False,
        )


############
# RAM TYPE #
############


class TestBbRamType(CommonMixin, TestCase):

    # Compatibility is True

    def test_ram_type_in_cpu_and_mb_comp_is_true(self):
        """check `RAM type` of `cpu` & `motherboard` compatibility"""

        first = ("DDR4", "DDR3")
        second = "DDR4"

        self.base(
            Cpu(ram_types=first),
            Motherboard(ram_type=second),
            RamTypeInCpuAndMotherboardCompRule(),
            f"ram type in `cpu` ({first}) and `motherboard` ({second})",
        )

    def test_ram_type_in_cpu_and_ram_comp_is_true(self):
        """check `RAM type` of `cpu` & `ram` compatibility"""

        first = ("DDR4", "DDR3")
        second = "DDR4"

        self.base(
            Cpu(ram_types=first),
            Ram(ram_type=second),
            RamTypeInCpuAndRamCompRule(),
            f"ram type in `cpu` ({first}) and `ram` ({second})",
        )

    def test_ram_type_in_motherboard_and_ram_comp_is_true(self):
        """check `RAM type` of `motherboard` & `ram` compatibility"""

        first = "DDR4"
        second = "DDR4"

        self.base(
            Motherboard(ram_type=first),
            Ram(ram_type=second),
            RamTypeInMotherboardAndRamCompRule(),
            f"ram type in `motherboard` ({first}) and `ram` ({second})",
        )

    # Compatibility is False

    def test_ram_type_in_cpu_and_mb_comp_is_false(self):
        """check `RAM type` of `cpu` & `motherboard` compatibility"""

        first = ("DDR4", "DDR3")
        second = "DDR5"

        self.base(
            Cpu(ram_types=first),
            Motherboard(ram_type=second),
            RamTypeInCpuAndMotherboardCompRule(),
            f"ram type in `cpu` ({first}) and `motherboard` ({second})",
            exp_compatibility=False,
        )

    def test_ram_type_in_cpu_and_ram_comp_is_false(self):
        """check `RAM type` of `cpu` & `ram` compatibility"""

        first = ("DDR4", "DDR3")
        second = "DDR5"

        self.base(
            Cpu(ram_types=first),
            Ram(ram_type=second),
            RamTypeInCpuAndRamCompRule(),
            f"ram type in `cpu` ({first}) and `ram` ({second})",
            exp_compatibility=False,
        )

    def test_ram_type_in_motherboard_and_ram_comp_is_false(self):
        """check `RAM type` of `motherboard` & `ram` compatibility"""

        first = "DDR4"
        second = "DDR5"

        self.base(
            Motherboard(ram_type=first),
            Ram(ram_type=second),
            RamTypeInMotherboardAndRamCompRule(),
            f"ram type in `motherboard` ({first}) and `ram` ({second})",
            exp_compatibility=False,
        )


#######
# PSU #
#######


class TestPsuCompatibilityRules(CommonMixin, TestCase):

    # ATX

    def test_atx_slot_in_psu_and_mb_comp_is_true(self):
        rule = MotherboardPowerCompRule()
        build = Build(
            motherboard=Motherboard(power_atx_slots=ComponentPowerSlots("ATX", [24]))
        )

        build.psu = PowerSupply(connectors=[PowerConnector("ATX", (20, 4))])
        self.assertTrue(rule.check(build).compatible)

        build.psu = PowerSupply(connectors=[PowerConnector("ATX", (24,))])
        self.assertTrue(rule.check(build).compatible)

    def test_atx_slot_in_psu_and_mb_comp_is_false(self):
        rule = MotherboardPowerCompRule()
        build = Build(
            motherboard=Motherboard(power_atx_slots=ComponentPowerSlots("ATX", [20]))
        )

        build.psu = PowerSupply(connectors=[PowerConnector("ATX", (24,))])
        self.assertFalse(rule.check(build).compatible)

    # EPS

    def test_eps_slot_in_psu_and_mb_comp_is_true(self):
        rule = MotherboardCpuPowerCompRule()
        build = Build(
            motherboard=Motherboard(power_eps_slots=ComponentPowerSlots("EPS", [8, 4])),
        )

        build.psu = PowerSupply(connectors=[PowerConnector("EPS", (8, 4))])
        self.assertTrue(rule.check(build).compatible)

        build.psu = PowerSupply(
            connectors=[PowerConnector("EPS", (4, 4)), PowerConnector("EPS", (4, 4))]
        )
        self.assertTrue(rule.check(build).compatible)

        build.psu = PowerSupply(
            connectors=[PowerConnector("EPS", (8, 8)), PowerConnector("EPS", (4, 4))]
        )
        self.assertTrue(rule.check(build).compatible)

    def test_eps_slot_in_psu_and_mb_comp_is_false(self):
        rule = MotherboardCpuPowerCompRule()
        build = Build(
            motherboard=Motherboard(power_eps_slots=ComponentPowerSlots("EPS", [8, 8])),
        )

        build.psu = PowerSupply(connectors=[PowerConnector("EPS", (8, 4))])
        self.assertFalse(rule.check(build).compatible)

        build.psu = PowerSupply(
            connectors=[PowerConnector("EPS", (4, 4)), PowerConnector("EPS", (10,))]
        )
        self.assertFalse(rule.check(build).compatible)

    # GPU

    def test_gpu_slot_in_psu_and_mb_comp_is_true(self):
        rule = GpuPowerCompRule()
        build = Build(gpu=Gpu(power_slots=ComponentPowerSlots("PCIe", [8, 6])))
        pcie = PowerConnector("PCIe", (6, 2))

        build.psu = PowerSupply(connectors=[pcie, pcie, pcie])
        self.assertTrue(rule.check(build).compatible)

        build.psu = PowerSupply(connectors=[pcie, pcie])
        self.assertTrue(rule.check(build).compatible)

    def test_gpu_slot_in_psu_and_mb_comp_is_false(self):
        rule = GpuPowerCompRule()
        build = Build(gpu=Gpu(power_slots=ComponentPowerSlots("PCIe", [8, 8, 6])))
        pcie = PowerConnector("PCIe", (6, 2))
        pcie6 = PowerConnector("PCIe", (6,))

        build.psu = PowerSupply(connectors=[pcie, pcie])
        self.assertFalse(rule.check(build).compatible)

        build.psu = PowerSupply(connectors=[pcie, pcie6, pcie6])
        self.assertFalse(rule.check(build).compatible)

        build.psu = PowerSupply(connectors=[pcie, pcie, PowerConnector("PCIe", (20,))])
        self.assertFalse(rule.check(build).compatible)


class TestPsuWattageCompatibilityRules(TestCase):
    """Перевірка потужності PSU"""

    def setUp(self):
        self.rule = PsuWattageRule()
        build = Build()

        build.cpu = Cpu(tdp_max=200)
        build.motherboard = Motherboard(manufacturer="MSI")
        build.ram = Ram(memory_modules=2, count=2)  # 4 modules
        build.gpu = Gpu(power=300)

        self.build = build

    def test_psu_wattage_when_not_psu_comp_is_true(self):
        """перевіряє коли psu немає"""

        self.assertTrue(self.rule.check(self.build).compatible)

    def test_psu_wattage_comp_is_true(self):
        """перевіряє коли Є psu"""

        self.build.psu = PowerSupply(power=900)

        self.assertTrue(self.rule.check(self.build).compatible)

    def test_psu_wattage_comp_is_false(self):
        """перевіряє коли psu слабкий"""

        self.build.psu = PowerSupply(power=400)

        response = self.rule.check(self.build)
        self.assertFalse(response.compatible)
        pprint(response)


class TestBuildRules(TestCase):
    def setUp(self):
        self.rules = compatibility_rules

        print(end="\n\n")

    def test_aa_build_with_many_components_and_rules_true(self):
        """"""

        cpu_manufacturer, mb_platform = "AMD", "AMD"
        socket = "AM4"
        cpu_ram_types, ram_type = ("DDR4",), "DDR4"
        cpu_codename, mb_codenames = "Rocket Lake", ("Rocket Lake", "Comet Lake")

        psu_pcie_conn = PowerConnector("PCIe", (6, 2))
        psu_atx_conn = PowerConnector("ATX", [20, 4])
        psu_epc_conn = PowerConnector("EPS", [8, 4])
        mb_power_atx_slots = ComponentPowerSlots("ATX", [24])
        mb_power_eps_slots = ComponentPowerSlots("EPS", [8, 4])
        gpu_power_slots = ComponentPowerSlots("EPS", [8, 6])

        psu = PowerSupply(
            connectors=[psu_atx_conn, psu_epc_conn, psu_pcie_conn, psu_pcie_conn]
        )

        build = Build(
            cpu=Cpu(
                manufacturer=cpu_manufacturer,
                socket=socket,
                ram_types=cpu_ram_types,
                codename=cpu_codename,
            ),
            motherboard=Motherboard(
                platform=mb_platform,
                socket=socket,
                ram_type=ram_type,
                cpu_codenames=mb_codenames,
                power_atx_slots=mb_power_atx_slots,
                power_eps_slots=mb_power_eps_slots,
            ),
            ram=Ram(ram_type=ram_type),
            gpu=Gpu(power_slots=gpu_power_slots),
            psu=psu,
        )

        for rule in self.rules:
            rule = rule()
            comp = rule.check(build).compatible
            # print(rule, "\t\t", rule.check(build).compatible)
            self.assertTrue(comp)

    def test_ab_build_with_many_components_and_rules_false(self):
        """"""

        cpu_man, mb_platform = "Intel", "AMD"
        cpu_socket, mb_socket = "LGA1200", "AM4"
        cpu_ram_types, mb_ram_type, ram_type = ("DDR4",), "DDR5", "DDR3"
        cpu_codename, mb_codenames = "Picasso", ("Rocket Lake", "Comet Lake")

        psu_pcie_conn = PowerConnector("PCIe", (6,))
        psu_atx_conn = PowerConnector("ATX", [20])
        psu_epc_conn = PowerConnector("EPS", [8, 4])
        mb_power_atx_slots = ComponentPowerSlots("ATX", [24])
        mb_power_eps_slots = ComponentPowerSlots("EPS", [8, 8])
        gpu_power_slots = ComponentPowerSlots("EPS", [8, 8, 8])

        psu = PowerSupply(
            connectors=[psu_atx_conn, psu_epc_conn, psu_pcie_conn, psu_pcie_conn]
        )

        build = Build(
            cpu=Cpu(
                manufacturer=cpu_man,
                socket=cpu_socket,
                ram_types=cpu_ram_types,
                codename=cpu_codename,
            ),
            motherboard=Motherboard(
                platform=mb_platform,
                socket=mb_socket,
                ram_type=mb_ram_type,
                cpu_codenames=mb_codenames,
                power_atx_slots=mb_power_atx_slots,
                power_eps_slots=mb_power_eps_slots,
            ),
            ram=Ram(ram_type=ram_type),
            gpu=Gpu(power_slots=gpu_power_slots),
            psu=psu,
        )

        for rule in self.rules:
            rule = rule()
            comp = rule.check(build).compatible

            self.assertFalse(comp)
