from unittest import TestCase

from src.compatibilities.rules import (
    SocketCompatibilityRule,
)
from src.compatibilities import exceptions as e
from src.tests.data.cpus import *
from src.tests.data.motherboards import *


class TestCpuCompatibilitiesRules(TestCase):

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
