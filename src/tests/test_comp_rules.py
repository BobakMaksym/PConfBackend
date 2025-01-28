from dataclasses import dataclass
from unittest import TestCase

from src.compatibilities.rules import (
    CompatibilityRuleInterface,
    # platform
    PlatformCpuAndMotherboardCompRule,
    # socket
    SocketCpuAndMotherboardCompRule,
    # ram
    RamTypeInCpuAndMotherboardCompRule,
    RamTypeInCpuAndRamCompRule,
    RamTypeInMotherboardAndRamCompRule,
)
from src.compatibilities import exceptions as e
from src.domain.base import Component
from src.domain.build import Build
from src.domain.enums import ComponentType


@dataclass
class Cpu:
    art: str = None
    manufacturer: str = None
    model: str = None
    series: str = None

    socket: str = None
    tdp: int = None
    ram_type: str = None
    max_ram: int = None
    _type = ComponentType.cpu


@dataclass
class Ram:
    art: str | None = None
    model: str | None = None
    manufacturer: str | None = None
    series: str | None = None

    ram_type: str | None = None
    speed: int | None = None
    kit: int | None = None
    kit_total_capacity: int | None = None

    _type = ComponentType.ram


@dataclass
class Motherboard:
    model: str = None
    manufacturer: str = None
    series: str = None  # Aorus/Gaming/Tuf

    platform: str = None  # Intel/AMD
    socket: str = None
    ram_type: str = None
    max_ram: int = None

    chipset: str = None
    _type = ComponentType.motherboard


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


############
# RAM TYPE #
############


class TestBbRamType(CommonMixin, TestCase):

    # Compatibility is True

    def test_ram_type_in_cpu_and_mb_comp_is_true(self):
        """check `RAM type` of `cpu` & `motherboard` compatibility"""

        first = "DDR4"
        second = "DDR4"

        self.base(
            Cpu(ram_type=first),
            Motherboard(ram_type=second),
            RamTypeInCpuAndMotherboardCompRule(),
            f"ram type in `cpu` ({first}) and `motherboard` ({second})",
        )

    def test_ram_type_in_cpu_and_ram_comp_is_true(self):
        """check `RAM type` of `cpu` & `ram` compatibility"""

        first = "DDR4"
        second = "DDR4"

        self.base(
            Cpu(ram_type=first),
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

        first = "DDR4"
        second = "DDR5"

        self.base(
            Cpu(ram_type=first),
            Motherboard(ram_type=second),
            RamTypeInCpuAndMotherboardCompRule(),
            f"ram type in `cpu` ({first}) and `motherboard` ({second})",
            exp_compatibility=False,
        )

    def test_ram_type_in_cpu_and_ram_comp_is_false(self):
        """check `RAM type` of `cpu` & `ram` compatibility"""

        first = "DDR4"
        second = "DDR5"

        self.base(
            Cpu(ram_type=first),
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


class TestBuildRules(TestCase):
    def setUp(self):
        self.rules = (
            SocketCpuAndMotherboardCompRule,
            PlatformCpuAndMotherboardCompRule,
            RamTypeInCpuAndMotherboardCompRule,
            RamTypeInCpuAndRamCompRule,
            RamTypeInMotherboardAndRamCompRule,
        )

        print(end="\n\n")

    def test_aa_build_with_many_components_and_rules_true(self):
        """"""

        build = Build()

        cpu_manufacturer, mb_platform = "AMD", "AMD"
        socket = "AM4"
        ram_type = "DDR4"

        cpu = Cpu(manufacturer=cpu_manufacturer, socket=socket, ram_type=ram_type)
        mb = Motherboard(platform=mb_platform, socket=socket, ram_type=ram_type)
        ram = Ram(ram_type=ram_type)

        build.cpu = cpu
        build.motherboard = mb
        build.ram = ram

        for rule in self.rules:
            rule = rule()
            comp = rule.check(build).compatible

            print(rule.__class__.__name__, comp)

    def test_ab_build_with_many_components_and_rules_false(self):
        """"""

        build = Build()

        cpu_man, mb_platform = "Intel", "AMD"
        cpu_socket, mb_socket = "LGA1200", "AM4"
        cpu_ram_type, mb_ram_type, ram_type = "DDR4", "DDR5", "DDR3"

        cpu = Cpu(manufacturer=cpu_man, socket=cpu_socket, ram_type=cpu_ram_type)
        mb = Motherboard(platform=mb_platform, socket=mb_socket, ram_type=mb_ram_type)
        ram = Ram(ram_type=ram_type)

        build.cpu = cpu
        build.motherboard = mb
        build.ram = ram

        for rule in self.rules:
            rule = rule()
            comp = rule.check(build).compatible

            print(rule.__class__.__name__, comp)


"""
int_cpu = Cpu("Intel", "LGA1200")
amd_cpu = Cpu("AMD", "AM4")

amd_mb = Motherboard("MSI", "AM4")
int_mb = Motherboard("Acer", "LGA1200")
"""
