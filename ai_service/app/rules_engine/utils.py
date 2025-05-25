def calculate_components_power_sum(build) -> int:
    """
    Обчислює споживання всіх компонентів збірки.
    Компоненти, для яких важко знайти значення споживання, мають стандартні значення
    """

    MB_POWER = 80
    RAM_MODULE_POWER = 4
    M2_SSD_POWER = 9
    SATA_POWER = 15
    FUN_POWER = 5

    TOTAL_CONSUMPTION = 0

    if build.cpu:
        if build.cpu.tdp_max:
            TOTAL_CONSUMPTION += build.cpu.tdp_max
        else:
            TOTAL_CONSUMPTION += build.cpu.tdp

    if build.motherboard:
        TOTAL_CONSUMPTION += MB_POWER

    if build.ram:
        # modules count in the kit * number of kit * power draw
        TOTAL_CONSUMPTION += build.ram.modules * RAM_MODULE_POWER
        # ram_power = ram.memory_modules * ram.count * RAM_MODULE_POWER

    if build.gpu:
        TOTAL_CONSUMPTION += build.gpu.power_consumption

    return TOTAL_CONSUMPTION
