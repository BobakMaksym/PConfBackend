from dataclasses import asdict
from pprint import pprint
from unittest import TestCase

from src.compatibilities.manager import compatibility_manager

from src.domain.models import Build, Cpu, Motherboard, Ram


class TestBuildRules(TestCase):
    def setUp(self):
        print(end="\n\n")

    def test_aa_build_with_many_components_and_rules_true(self):
        """"""

        cpu_manufacturer, mb_platform = "AMD", "AMD"
        socket = "AM4"
        cpu_ram_types, ram_type = ("DDR4",), "DDR4"
        cpu_codename, mb_codenames = "Rocket Lake", ("Rocket Lake", "Comet Lake")

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
            ),
            ram=Ram(ram_type=ram_type),
        )

        compatibility_manager.check_compatibility(build)

    def test_ab_build_with_many_components_and_rules_false(self):
        """"""

        cpu_man, mb_platform = "Intel", "AMD"
        cpu_socket, mb_socket = "LGA1200", "AM4"
        cpu_ram_types, mb_ram_type, ram_type = ("DDR4",), "DDR5", "DDR3"
        cpu_codename, mb_codenames = "Picasso", ("Rocket Lake", "Comet Lake")

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
            ),
            ram=Ram(ram_type=ram_type),
        )

        pprint(asdict(build.errors))
        print(end="\n\n")

        compatibility_manager.check_compatibility(build)

        pprint(asdict(build.errors))
