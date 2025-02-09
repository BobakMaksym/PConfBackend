from abc import ABC, abstractmethod

from src.compatibilities.rule.utils import (
    allocate_requirements,
    get_cables,
    calculate_components_power_sum,
)
from src.compatibilities.rule.response import CompRuleResponse
from src.domain.models import Build, Cpu, Gpu, Motherboard, Ram
from src.domain.models import ComponentType as CT


class CompatibilityRuleInterface(ABC):
    @abstractmethod
    def check(self, build: Build, component_count: int = 1) -> CompRuleResponse:
        """checks if the new component is compatible with the already selected ones"""
        pass


class SocketCpuAndMotherboardCompRule(CompatibilityRuleInterface):
    def check(self, build: Build) -> CompRuleResponse:
        """checks the `socket` compatibility of `cpu` and `motherboard`"""

        cpu, mb = build.cpu, build.motherboard

        # якщо додані всі (cpu, motherboard)
        if all((cpu, mb)):
            cpu_sock, mb_sock = cpu.socket, mb.socket
            if cpu_sock != mb_sock:  # порівняння значень
                err = f"сокет cpu ({cpu_sock}) не сумісний з сокетом плати ({mb_sock})"
                errors = {CT.cpu.value: err, CT.motherboard.value: err}

                return CompRuleResponse(False, errors)

        # якщо потірбні компоенети не додані, значить помилок буде не може
        return CompRuleResponse(True)


class PlatformCpuAndMotherboardCompRule(CompatibilityRuleInterface):
    def check(self, build: Build) -> CompRuleResponse:
        """checks the `platform` compatibility of `cpu` and `motherboard`"""

        cpu, mb = build.cpu, build.motherboard

        if all((cpu, mb)):
            # cpu.manufacturer == mb.platform; should be like `amd` & `amd`
            cpu_val, mb_val = cpu.manufacturer, mb.platform
            if cpu_val != mb_val:  # порівняння значень
                err = f"cpu platform ({cpu_val}) not compatible with mb platform ({mb_val})"
                errors = {CT.cpu.value: err, CT.motherboard.value: err}

                return CompRuleResponse(False, errors)

        return CompRuleResponse(True)


class MotherboardChipsetSupportsCpuRule(CompatibilityRuleInterface):
    def check(self, build: Build) -> CompRuleResponse:
        """checks whether the `motherboard` supports the `cpu` by `codename`, for example, Raptor Lake"""

        cpu, mb = build.cpu, build.motherboard

        if all((cpu, mb)):
            codename, codenames = cpu.codename, mb.cpu_codenames
            if codename not in codenames:
                err = f"""The "{codename}" cpu core is not supported by the
                motherboard chipset that supports "{codenames}" """
                errors = {CT.cpu.value: err, CT.motherboard.value: err}

                return CompRuleResponse(False, errors)

        return CompRuleResponse(True)


# RAM TYPE IN CPU, MOTHERBOARD, RAM


class RamTypeInCpuAndMotherboardCompRule(CompatibilityRuleInterface):
    def check(self, build: Build) -> CompRuleResponse:
        """checks the `ram type` compatibility of `cpu` and `motherboard`"""

        # cpu, mb, ram = build.cpu, build.motherboard, build.ram
        cpu, mb = build.cpu, build.motherboard

        if all((cpu, mb)):
            # cpu.ram_type == mb.ram_type; should be like `DDR4` & `DDR4`
            types, type_ = cpu.ram_types, mb.ram_type
            if type_ not in types:  # порівняння значень
                err = f"cpu's ram type ({types}) != motherboard's ram type ({type_})"
                errors = {CT.cpu.value: err, CT.motherboard.value: err}

                return CompRuleResponse(False, errors)

        return CompRuleResponse(True)


class RamTypeInCpuAndRamCompRule(CompatibilityRuleInterface):
    def check(self, build: Build) -> CompRuleResponse:
        """checks the `ram type` compatibility of `cpu` and `ram`"""

        cpu, ram = build.cpu, build.ram

        if all((cpu, ram)):
            # cpu.ram_type == ram.ram_type; should be like `DDR4` & `DDR4`
            types, type_ = cpu.ram_types, ram.ram_type
            if type_ not in types:  # порівняння значень
                err = f"cpu's ram type ({types}) != ram's type ({type_})"
                errors = {CT.cpu.value: err, CT.ram.value: err}

                return CompRuleResponse(False, errors)

        return CompRuleResponse(True)


class RamTypeInMotherboardAndRamCompRule(CompatibilityRuleInterface):
    def check(self, build: Build) -> CompRuleResponse:
        """checks the `ram type` compatibility of `motherboard` and `ram`"""

        motherboard, ram = build.motherboard, build.ram

        if all((motherboard, ram)):
            val_1, val_2 = motherboard.ram_type, ram.ram_type
            if val_1 != val_2:
                err = f"motherboard's ram type ({val_1}) != ram's type ({val_2})"
                errors = {CT.motherboard.value: err, CT.ram.value: err}

                return CompRuleResponse(False, errors)

        return CompRuleResponse(True)


# PSU connectors


class MotherboardPowerCompRule(CompatibilityRuleInterface):
    """Перевірка сумісності живлення материнської плати (ATX)."""

    def check(self, build: Build) -> CompRuleResponse:
        md, psu = build.motherboard, build.psu

        if not (md and psu):
            return CompRuleResponse(True)
        # наприклад, [24] або [20] (якщо використовується лише 20 пінів)
        requirements = md.power_atx_slots.slots
        cables = get_cables(psu, "ATX")
        if allocate_requirements(requirements, cables):
            return CompRuleResponse(True)
        else:
            msg = f"БЖ не має сумісного ATX живлення для {requirements}"
            return CompRuleResponse(False, {"motherboard": msg})


class MotherboardCpuPowerCompRule(CompatibilityRuleInterface):
    """Перевірка живлення процесора (EPS)."""

    def check(self, build: Build) -> CompRuleResponse:
        mb, psu = build.motherboard, build.psu

        if not (mb and psu):
            return CompRuleResponse(True)
        requirements = mb.power_eps_slots.slots  # наприклад, [8] або [8, 8]
        cables = get_cables(psu, "EPS")
        if allocate_requirements(requirements, cables):
            return CompRuleResponse(True)
        else:
            msg = f"БЖ не має сумісного EPS живлення для {requirements}"
            return CompRuleResponse(False, {"cpu": msg})


class GpuPowerCompRule(CompatibilityRuleInterface):
    """Перевірка живлення відеокарти (PCIe)."""

    def check(self, build: Build) -> CompRuleResponse:
        gpu, psu = build.gpu, build.psu

        if not (gpu and psu):
            return CompRuleResponse(True)
        requirements = gpu.power_slots.slots  # наприклад, [8, 6]
        cables = get_cables(psu, "PCIe")
        if allocate_requirements(requirements, cables):
            return CompRuleResponse(True)
        else:
            msg = f"БЖ не має сумісного PCIe живлення для {requirements}"
            return CompRuleResponse(False, {"gpu": msg})


class PsuWattageRule(CompatibilityRuleInterface):
    """Перевіряє, чи потужність БЖ достатня для всіх компонентів збірки"""

    SAFETY_MARGIN = 1.2  # recommended power reserve (20%)

    def check(self, build: Build) -> CompRuleResponse:
        if not build.psu:
            return CompRuleResponse(True)  # Якщо БЖ немає, немає сенсу перевіряти

        total_power_draw = calculate_components_power_sum(build)

        required_wattage = total_power_draw * self.SAFETY_MARGIN
        psu_power = build.psu.power

        if psu_power < required_wattage:
            err = f"БЖ ({psu_power}W) занадто слабкий. Мінімум потрібно {required_wattage:.0f}W."
            return CompRuleResponse(False, {CT.psu.value: err})

        return CompRuleResponse(True)


class PsuEfficiencyRule(CompatibilityRuleInterface):
    """Перевіряє, чи потужність БЖ не надто велика або мала"""

    MIN_LOAD = 0.5  # Мінімальне рекомендоване навантаження (50%)
    MAX_LOAD = 0.8  # Максимальне рекомендоване навантаження (80%)

    def check(self, build: Build) -> CompRuleResponse:
        if not build.psu:
            return CompRuleResponse(True)

        total_power_draw = calculate_components_power_sum(build)

        psu_wattage = build.psu.power
        load_ratio = total_power_draw / psu_wattage

        if load_ratio < self.MIN_LOAD:
            err = f"БЖ ({psu_wattage}W) занадто потужний. Використовується лише {load_ratio:.0%} його потужності."
            return CompRuleResponse(False, {CT.psu.value: err})

        if load_ratio > self.MAX_LOAD:
            err = f"БЖ ({psu_wattage}W) може працювати на межі можливостей ({load_ratio:.0%} навантаження)."
            return CompRuleResponse(False, {CT.psu.value: err})

        return CompRuleResponse(True)


rules = (
    PlatformCpuAndMotherboardCompRule,
    SocketCpuAndMotherboardCompRule,
    MotherboardChipsetSupportsCpuRule,
    RamTypeInCpuAndMotherboardCompRule,
    RamTypeInCpuAndRamCompRule,
    RamTypeInMotherboardAndRamCompRule,
    MotherboardPowerCompRule,
    MotherboardCpuPowerCompRule,
    # GpuPowerCompRule,
    # PsuEfficiencyRule,
)
