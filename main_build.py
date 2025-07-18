from app.schemas.component_schema import *


if __name__ == "__main__":

    cpu = Cpu(
        manufacturer="AMD",
        model="Ryzen 5 5600X",
        socket="AM4",
        ram_types="DDR4",
        igp=False,
        tdp=65,
        tdp_max=88,
        cores=6,
        threads=12,
    )
    ram = Ram(
        manufacturer="Corsair",
        model="Vengeance LPX",
        type="DDR5",
        modules=2,
        capacity=16,  # 16 GB total
        speed=3200,  # in MHz
    )
    gpu = Gpu(
        manufacturer="NVIDIA",
        model="GeForce RTX 3060",
        model_gpu="GA106",
        memory_size=12,  # in GB
        memory_type="GDDR6",
        power_consumption=170,  # in W
    )
    motherboard = Motherboard(
        manufacturer="MSI",
        model="B550M PRO-VDH WIFI",
        socket="AM5",
        form_factor="mATX",
        ram_type="DDR4",
        ram_slots=4,
        m2_count=2,
        chipset="B550",
    )
    psu = PowerSupply(
        manufacturer="be quiet!",
        model="Pure Power 12 M",
        form_factor="ATX",
        power=200,
        mb_and_cpu_powersupply="24+8 pin",
        plus_12v=200,  # in W
    )

    build = PcConfig()

    build.cpu = cpu
    build.update_errors()

    build.ram = ram
    # build.update_errors()

    build.psu = psu
    # build.update_errors()

    build.gpu = gpu
    # build.update_errors()

    print(build.model_dump())
