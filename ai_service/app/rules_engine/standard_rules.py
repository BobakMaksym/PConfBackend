# rules_engine/standard_rules.py
from .core import Rule, register
from .utils import calculate_components_power_sum


class SocketCompatibility(Rule):
    def validate(self, build):
        if build.cpu and build.motherboard:
            if build.cpu.socket.lower() != build.motherboard.socket.lower():
                return [
                    f"Несумісні сокети: CPU `{build.cpu.socket}` ≠ MB `{build.motherboard.socket}`"
                ]
        return []


class RamTypeMatches(Rule):
    def validate(self, build):

        errors = []

        if build.cpu and build.ram:
            if build.ram.type not in build.cpu.ram_types:
                msg = f"RAM `{build.ram.type}` не підтримується CPU `{build.cpu.ram_types}`"
                errors.append(msg)

        if build.motherboard and build.ram:
            if build.ram.type != build.motherboard.ram_type:
                msg = f"RAM `{build.ram.type}` ≠ MB `{build.motherboard.ram_type}`"
                errors.append(msg)

        if build.cpu and build.motherboard:
            if build.motherboard.ram_type not in build.cpu.ram_types:
                msg = f"MB `{build.motherboard.ram_type}` не підтрипує CPU `{build.cpu.ram_types}`"
                errors.append(msg)

        return errors


class PsuPowerSufficiency(Rule):
    """Перевіряє, чи потужність БЖ достатня для всіх компонентів збірки"""

    SAFETY_MARGIN = 0.2  # recommended power reserve (20%)

    def validate(self, build):

        errors = []

        if not build.psu:
            return []  # Якщо БЖ немає, немає сенсу перевіряти

        total_power_draw = calculate_components_power_sum(build)

        required_wattage = total_power_draw * (1 + self.SAFETY_MARGIN)
        psu_power = build.psu.power

        if psu_power < required_wattage:
            msg = f"БЖ ({psu_power}W) занадто слабкий. Мінімум потрібно {required_wattage:.0f}W."
            errors.append(msg)

        return errors


register(SocketCompatibility())
register(RamTypeMatches())
register(PsuPowerSufficiency())
