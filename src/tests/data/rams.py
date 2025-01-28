from src.domain.models import Ram


ram_1 = Ram(
    art="F4-3600C18D-16GTZRX",
    model="Trident Z RGB",
    manufacturer="G.SKILL",
    series="Trident Z",
    ram_type="DDR4",
    speed=3600,
    kit=2,
    kit_total_capacity=16,
)

ram_2 = Ram(
    art="CMW32GX4M2E3200C16",
    model="Vengeance RGB Pro",
    manufacturer="Corsair",
    series="Vengeance RGB Pro",
    ram_type="DDR4",
    speed=3200,
    kit=2,
    kit_total_capacity=32,
)

ram_3 = Ram(
    art="KF552C40BBK2-32",
    model="Fury Beast",
    manufacturer="Kingston",
    series="Fury Beast",
    ram_type="DDR5",
    speed=5200,
    kit=2,
    kit_total_capacity=32,
)

ram_4 = Ram(
    art="HX432C16FB3K2/16",
    model="HyperX Fury",
    manufacturer="HyperX",
    series="Fury",
    ram_type="DDR4",
    speed=3200,
    kit=2,
    kit_total_capacity=16,
)

ram_5 = Ram(
    art="BL2K16G36C16U4R",
    model="Ballistix",
    manufacturer="Crucial",
    series="Ballistix",
    ram_type="DDR4",
    speed=3600,
    kit=2,
    kit_total_capacity=32,
)

ram_6 = Ram(
    art="CMK32GX5M2B5200C40",
    model="Vengeance",
    manufacturer="Corsair",
    series="Vengeance",
    ram_type="DDR5",
    speed=5200,
    kit=2,
    kit_total_capacity=32,
)

ram_db = [ram_1, ram_2, ram_3, ram_4, ram_5, ram_6]

if __name__ == "__main__":
    for item in ram_db:
        print(item)
