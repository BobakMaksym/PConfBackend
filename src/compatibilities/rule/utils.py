from src.domain.models import (
    Build,
    PowerSupply,
    PSUCable,
    ComponentType as CT,
    Cpu,
    Motherboard,
    Gpu,
    Ram,
)


# ==================== Нова модель для кабелю БЖ ====================


def get_cables(psu: PowerSupply, connector_type: str) -> list[PSUCable]:
    """
    Перетворює конектори БЖ у список PSUCable для певного типу.
    """

    cabels = []
    for connector in psu.connectors:
        if connector.type == connector_type:
            cabels.append(PSUCable(connector.type, list(connector.pins)))

    return cabels

    # return [
    #     PSUCable(connector.type, list(connector.pins))
    #     for connector in psu.connectors
    #     if connector.type == connector_type
    # ]


# ==================== Допоміжні функції для розподілу ====================


def find_combinations(
    available: list[int], target: int, start: int = 0, current: list[int] = None
):
    """
    Рекурсивно перебирає індекси зі списку available, сума яких дорівнює target.
    Повертає всі можливі комбінації індексів.
    """
    if current is None:
        current = []
    if target == 0:
        yield current.copy()
        return
    for i in range(start, len(available)):
        if available[i] <= target:
            current.append(i)
            yield from find_combinations(
                available, target - available[i], i + 1, current
            )
            current.pop()


def allocate_requirements(requirements: list[int], cables: list[PSUCable]) -> bool:
    """
    Намагається розподілити список вимог (кількість пінів у слотах)
    між кабелями (кожен кабель може видати одну або декілька секцій,
    але якщо кабель не роздільний – його можна використати тільки один раз).
    Використовується backtracking.
    """
    # Сортуємо вимоги у спадаючому порядку для зменшення гілок перебору
    reqs_sorted = sorted(requirements, reverse=True)

    def backtrack(reqs: list[int], cables_state: list[PSUCable]) -> bool:
        if not reqs:
            return True  # всі вимоги задоволено

        r = reqs[0]
        for cable in cables_state:
            # Якщо кабель не має достатньої сумарної кількості пінів,
            # то пропускаємо його (для оптимізації)
            if sum(cable.available) < r:
                continue

            # Знаходимо всі комбінації індексів у cable.available, що дають суму r.
            for alloc in list(find_combinations(cable.available, r)):
                # Зробимо копію доступних секцій для backtracking
                old_available = cable.available.copy()
                # «Витрачаємо» ті секції – видаляємо їх з available
                cable.available = [
                    val for i, val in enumerate(cable.available) if i not in alloc
                ]
                if backtrack(reqs[1:], cables_state):
                    return True
                # Повертаємо стан назад
                cable.available = old_available
        return False

    # Щоб не змінювати початкові дані, клонуватимемо кожен кабель
    cables_state = [cable.clone() for cable in cables]
    return backtrack(reqs_sorted, cables_state)


# ==================== Допоміжні функції для розрахунку потужності PSU ====================


def calculate_components_power_sum(build: Build) -> int:
    """
    Обчислює споживання всіх компонентів збірки.
    Компоненти, для яких важко знайти значення споживання, мають стандартні значення
    """

    MB_POWER = 80
    RAM_MODULE_POWER = 4
    M2_SSD_POWER = 9
    SATA_POWER = 15
    FUN_POWER = 5

    components_power = []

    cpu: Cpu = getattr(build, CT.cpu.value)
    if cpu:
        if cpu.tdp_max:
            components_power.append(cpu.tdp_max)
        elif cpu.tdp:
            components_power.append(cpu.tdp)

    mb: Motherboard = getattr(build, CT.motherboard.value)
    if mb:
        components_power.append(MB_POWER)

    ram: Ram = getattr(build, CT.ram.value)
    if ram:
        # modules count in the kit * number of kit * power draw
        ram_power = ram.memory_modules * ram.count * RAM_MODULE_POWER
        components_power.append(ram_power)

    gpu: Gpu = getattr(build, CT.gpu.value)
    if gpu:
        components_power.append(gpu.power)

    total_power_draw = sum(components_power)
    return int(total_power_draw)
