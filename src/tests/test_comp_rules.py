from dataclasses import dataclass
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
    rules as compatibility_rules,
)
from src.domain.models import Component
from src.domain.models import Build
from src.domain.models import ComponentType, Cpu, Motherboard, Ram


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
        self.rules = compatibility_rules

        print(end="\n\n")

    def test_aa_build_with_many_components_and_rules_true(self):
        """"""

        cpu_manufacturer, mb_platform = "AMD", "AMD"
        socket = "AM4"
        ram_type = "DDR4"

        build = Build(
            cpu=Cpu(manufacturer=cpu_manufacturer, socket=socket, ram_type=ram_type),
            motherboard=Motherboard(
                platform=mb_platform, socket=socket, ram_type=ram_type
            ),
            ram=Ram(ram_type=ram_type),
        )

        for rule in self.rules:
            rule = rule()
            comp = rule.check(build).compatible

            self.assertTrue(comp)

    def test_ab_build_with_many_components_and_rules_false(self):
        """"""

        cpu_man, mb_platform = "Intel", "AMD"
        cpu_socket, mb_socket = "LGA1200", "AM4"
        cpu_ram_type, mb_ram_type, ram_type = "DDR4", "DDR5", "DDR3"

        build = Build(
            cpu=Cpu(manufacturer=cpu_man, socket=cpu_socket, ram_type=cpu_ram_type),
            motherboard=Motherboard(
                platform=mb_platform, socket=mb_socket, ram_type=mb_ram_type
            ),
            ram=Ram(ram_type=ram_type),
        )

        for rule in self.rules:
            rule = rule()
            comp = rule.check(build).compatible

            self.assertFalse(comp)
