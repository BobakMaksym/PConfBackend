from src.domain.models import Cpu


cpu_amd_r5_am4_tdp65 = Cpu(
    "100-000001801", "AMD", "AMD Ryzen™ 5 5605G", "Ryzen 5000", "AM4", 65, "DDR4", 128
)
cpu_amd_r7_am4_tdp105 = Cpu(
    "100-000001503",
    "AMD",
    "AMD Ryzen™ 7 5700X3D",
    "Ryzen 7000",
    "AM4",
    105,
    "DDR4",
    128,
)
cpu_amd_r7_am5_tdp105 = Cpu(
    "100-000000599",
    "AMD",
    "AMD Ryzen™ 7 PRO 7745",
    "Ryzen PRO 7000",
    "AM5",
    65,
    "DDR5",
    128,
)
cpu_intel_i5_12400_tdp65 = Cpu(
    "BX8071512400",
    "Intel",
    "Intel Core i5 12400",
    "Alder Lake",
    "LGA 1700",
    65,
    "DDR5",
    128,
)
cpu_intel_i9_10900F_tdp65 = Cpu(
    "CM8070104282625",
    "Intel",
    "Intel Core i9-10900F",
    "Comet Lake",
    "FCLGA1200",
    65,
    "DDR4",
    128,
)


# ############################################################

cpu_intel_i5_13600kf_ddr5 = Cpu(
    art="BX8071513600KF",
    manufacturer="Intel",
    model="i5-13600KF",
    series="Core i5",
    socket="LGA1700",
    tdp=125,
    ram_type="DDR4/DDR5",
    memory_channels=2,
)

cpu_intel_i9_13900k_ddr5 = Cpu(
    art="BX8071513900K",
    manufacturer="Intel",
    model="i9-13900K",
    series="Core i9",
    socket="LGA1700",
    tdp=125,
    ram_type="DDR4/DDR5",
    memory_channels=2,
)

cpu_intel_i7_13700k_ddr5 = Cpu(
    art="BX8071513700K",
    manufacturer="Intel",
    model="i7-13700K",
    series="Core i7",
    socket="LGA1700",
    tdp=125,
    ram_type="DDR4/DDR5",
    memory_channels=2,
)

cpu_intel_i5_12400f_ddr4 = Cpu(
    art="BX8071512400F",
    manufacturer="Intel",
    model="i5-12400F",
    series="Core i5",
    socket="LGA1700",
    tdp=65,
    ram_type="DDR4/DDR5",
    memory_channels=2,
)

cpu_intel_i3_12100f_ddr4 = Cpu(
    art="BX8071512100F",
    manufacturer="Intel",
    model="i3-12100F",
    series="Core i3",
    socket="LGA1700",
    tdp=65,
    ram_type="DDR4/DDR5",  # Підтримує обидва типи
    memory_channels=2,
)

cpu_intel_xeon_w9_3495x = Cpu(
    art="CD8071905118700",
    manufacturer="Intel",
    model="Xeon w9-3495X",
    series="Xeon W",
    socket="LGA4677",
    tdp=350,
    ram_type="DDR5",
    memory_channels=8,
)
cpu_intel_xeon_w7_2495x = Cpu(
    art="CD8071905202800",
    manufacturer="Intel",
    model="Xeon w7-2495X",
    series="Xeon W",
    socket="LGA1700",
    tdp=200,
    ram_type="DDR5",
    memory_channels=4,
)
cpu_intel_xeon_w5_2465x = Cpu(
    art="CD8071905202900",
    manufacturer="Intel",
    model="Xeon w5-2465X",
    series="Xeon W",
    socket="LGA1700",
    tdp=165,
    ram_type="DDR5",
    memory_channels=4,
)

cpus = [
    cpu_intel_i5_13600kf_ddr5,
    cpu_intel_i9_13900k_ddr5,
    cpu_intel_i7_13700k_ddr5,
    cpu_intel_i5_12400f_ddr4,
    cpu_intel_i3_12100f_ddr4,
    cpu_intel_xeon_w9_3495x,
    cpu_intel_xeon_w7_2495x,
    cpu_intel_xeon_w5_2465x,
]


if __name__ == "__main__":
    for item in cpus:
        print(item)
