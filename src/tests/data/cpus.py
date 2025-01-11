from src.domain.cpu import CPU


cpu_amd_r5_am4_tdp65 = CPU(
    "100-000001801", "AMD", "AMD Ryzen™ 5 5605G", "Ryzen 5000", "AM4", 65, "DDR4", 128
)
cpu_amd_r7_am4_tdp105 = CPU(
    "100-000001503",
    "AMD",
    "AMD Ryzen™ 7 5700X3D",
    "Ryzen 7000",
    "AM4",
    105,
    "DDR4",
    128,
)
cpu_amd_r7_am5_tdp105 = CPU(
    "100-000000599",
    "AMD",
    "AMD Ryzen™ 7 PRO 7745",
    "Ryzen PRO 7000",
    "AM5",
    65,
    "DDR5",
    128,
)
cpu_intel_i5_12400_tdp65 = CPU(
    "BX8071512400",
    "Intel",
    "Intel Core i5 12400",
    "Alder Lake",
    "LGA 1700",
    65,
    "DDR5",
    128,
)
cpu_intel_i9_10900F_tdp65 = CPU(
    "CM8070104282625",
    "Intel",
    "Intel Core i9-10900F",
    "Comet Lake",
    "FCLGA1200",
    65,
    "DDR4",
    128,
)


cpu_1 = CPU(
    art="100-100000597MPK",
    manufacturer="AMD",
    model="7500F",
    series="Ryzen 5",
    socket="AM5",
    tdp=65,
    ram_type="DDR5",
    max_ram=128,
    # cores=6,
    # threads=12,
)

cpu_2 = CPU(
    art="BX8071513600KF",
    manufacturer="Intel",
    model="i5-13600KF",
    series="Core i5",
    socket="LGA1700",
    tdp=125,
    ram_type="DDR5",
    max_ram=128,
    # cores=14,
    # threads=20,
)

cpu_3 = CPU(
    art="BX8071513700K",
    manufacturer="Intel",
    model="i7-13700K",
    series="Core i7",
    socket="LGA1700",
    tdp=125,
    ram_type="DDR4",
    max_ram=128,
    # cores=16,
    # threads=24,
)

cpu_4 = CPU(
    art="100-100000589WOF",
    manufacturer="AMD",
    model="5800X",
    series="Ryzen 7",
    socket="AM4",
    tdp=105,
    ram_type="DDR5",
    max_ram=128,
    # cores=8,
    # threads=16,
)

cpu_5 = CPU(
    art="BX8071512900K",
    manufacturer="Intel",
    model="i9-12900K",
    series="Core i9",
    socket="LGA1700",
    tdp=125,
    ram_type="DDR5",
    max_ram=128,
    # cores=16,
    # threads=24,
)

cpu_6 = CPU(
    art="100-100000795WOF",
    manufacturer="AMD",
    model="7950X",
    series="Ryzen 9",
    socket="AM5",
    tdp=170,
    ram_type="DDR4",
    max_ram=128,
    # cores=16,
    # threads=32,
)

cpu_db = [cpu_1, cpu_2, cpu_3, cpu_4, cpu_5, cpu_6]


if __name__ == "__main__":
    for item in cpu_db:
        print(item)
