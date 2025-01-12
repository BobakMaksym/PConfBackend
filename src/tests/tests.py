from unittest import TestCase

from src.compatibilities.rules import (
    SocketCompatibilityRule,
    RamTypeOfCpuAndMotherboardCompRule,
)
from src.compatibilities import exceptions as e
from src.tests.data.cpus import *
from src.tests.data.motherboards import *


class TestCpuCompatibilitiesRules(TestCase):

    # # Test platform compatibility

    # def test_aa_AMD_platform_CPUs_and_AMD_motherboard_than_comp_is_true(self):
    #     """test: check platform of motherboard & cpu"""

    #     rule = PlatformCompatibilityRule()

    #     amd_platform_CPUs = (
    #         cpu_amd_r5_am4_tdp65,
    #         cpu_amd_r7_am4_tdp105,
    #         cpu_amd_r7_am5_tdp105,
    #     )

    #     for cpu in amd_platform_CPUs:
    #         with self.subTest(cpu=cpu):
    #             self.assertTrue(
    #                 rule.is_compatible([mb_gigabyte_am5_ddr5_X870E], cpu),
    #                 f"Expected {cpu} to be compatible with {mb_gigabyte_am5_ddr5_X870E}",
    #             )

    # def test_ab_Intel_platform_CPUs_and_Intel_motherboard_than_comp_is_true(self):
    #     """test: check platform of motherboard & cpu"""

    #     rule = PlatformCompatibilityRule()

    #     intel_platform_CPUs = (
    #         cpu_intel_i5_12400_tdp65,
    #         cpu_intel_i9_10900F_tdp65,
    #         cpu_intel_xeon_w5_2465x,
    #     )

    #     motherboard = mb_msi_lga1700_z690

    #     for cpu in intel_platform_CPUs:
    #         with self.subTest(cpu=cpu):
    #             self.assertTrue(
    #                 rule.is_compatible([motherboard], cpu),
    #                 f"Expected {cpu} to be compatible with {motherboard}",
    #             )

    # def test_ac_AMD_CPUs_and_Intel_platform_motherboard_than_exception(self):
    #     """test: check platform of motherboard & cpu"""

    #     rule = PlatformCompatibilityRule()

    #     amd_platform_CPUs = (
    #         cpu_amd_r5_am4_tdp65,
    #         cpu_amd_r7_am4_tdp105,
    #         cpu_amd_r7_am5_tdp105,
    #     )
    #     intel_platform_motherboard = mb_msi_lga1700_z690

    #     for cpu in amd_platform_CPUs:
    #         with self.subTest(cpu=cpu):
    #             with self.assertRaises(e.PlatformCompatibilityException):
    #                 rule.is_compatible([intel_platform_motherboard], cpu)

    # Test socket compatibility

    def test_aa_given_cpu_and_motherboard_when_socket_matches_then_compatibility_is_true(
        self,
    ):
        """test: checks the compatibility of the cpu with the selected motherboard"""

        socket_rule = SocketCompatibilityRule()

        self.assertTrue(
            socket_rule.is_compatible(
                [mb_gigabyte_am5_ddr5_X870E], cpu_amd_r7_am5_tdp105
            )
        )

    def test_ab_given_cpu_and_motherboard_when_socket_not_match_then_not_compatibility(
        self,
    ):
        """test: checks if the cpu is not compatible with the selected motherboard"""

        socket_rule = SocketCompatibilityRule()

        selected_components = [mb_gigabyte_am5_ddr5_X870E]

        with self.assertRaises(e.SocketCompatibilityException):
            socket_rule.is_compatible(selected_components, cpu_intel_i9_10900F_tdp65)
        with self.assertRaises(e.SocketCompatibilityException):
            socket_rule.is_compatible(selected_components, cpu_amd_r5_am4_tdp65)

    # Test RAM type compatibility

    def test_ba_given_cpu_and_motherboard_when_ram_type_matches_then_compatibility_is_true(
        self,
    ):
        """test: checks for incompatibility of the cpu memory type with the selected motherboard"""

        # check the compatibility of the motherboard and CPU with support for the same types of memory
        # motherboard & cpu - DDR5

        rule = RamTypeOfCpuAndMotherboardCompRule()
        selected = [mb_gigabyte_am5_ddr5_X870E]

        self.assertTrue(rule.is_compatible(selected, cpu_amd_r7_am5_tdp105))
        self.assertTrue(rule.is_compatible(selected, cpu_intel_i5_12400_tdp65))

    def test_bb_given_cpu_and_motherboard_when_ram_type_not_matches_then_except(self):
        """test: checks for incompatibility of the cpu memory type with the selected motherboard"""

        # check the compatibility of the motherboard and CPU with support with support for different types of memory
        # motherboard - DDR5, cpu - DDR4

        rule = RamTypeOfCpuAndMotherboardCompRule()
        selected = [mb_gigabyte_am5_ddr5_X870E]

        with self.assertRaises(e.RamTypeCompatibilityException):
            rule.is_compatible(selected, cpu_amd_r5_am4_tdp65)
        with self.assertRaises(e.RamTypeCompatibilityException):
            rule.is_compatible(selected, cpu_intel_i9_10900F_tdp65)
