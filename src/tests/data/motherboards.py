from src.domain.mb import MotherBoard


mb_gigabyte_am5_ddr5_X870E = MotherBoard(
    "Gigabyte X870E AORUS XTREME",
    "Gigabyte",
    "AORUS",
    "AMD",
    "AM5",
    "DDR5",
    256,
    "X870E",
)


motherboard_1 = MotherBoard(
    model="ROG STRIX B550-F GAMING",
    manufacturer="ASUS",
    series="ROG",
    platform="AMD",
    socket="AM4",
    ram_type="DDR4",
    max_ram=128,
    chipset="B550",
)

motherboard_2 = MotherBoard(
    model="MSI MPG Z690 EDGE WIFI",
    manufacturer="MSI",
    series="MPG",
    platform="Intel",
    socket="LGA1700",
    ram_type="DDR5",
    max_ram=128,
    chipset="Z690",
)

motherboard_3 = MotherBoard(
    model="GIGABYTE B450M DS3H",
    manufacturer="GIGABYTE",
    series="Ultra Durable",
    platform="AMD",
    socket="AM4",
    ram_type="DDR4",
    max_ram=64,
    chipset="B450",
)

motherboard_4 = MotherBoard(
    model="ASROCK Z590 EXTREME",
    manufacturer="ASRock",
    series="Extreme",
    platform="Intel",
    socket="LGA1200",
    ram_type="DDR4",
    max_ram=128,
    chipset="Z590",
)

motherboard_5 = MotherBoard(
    model="AORUS X670E MASTER",
    manufacturer="GIGABYTE",
    series="AORUS",
    platform="AMD",
    socket="AM5",
    ram_type="DDR5",
    max_ram=128,
    chipset="X670E",
)

motherboard_6 = MotherBoard(
    model="TUF GAMING Z790-PLUS",
    manufacturer="ASUS",
    series="TUF",
    platform="Intel",
    socket="LGA1700",
    ram_type="DDR5",
    max_ram=128,
    chipset="Z790",
)

motherboard_db = [
    motherboard_1,
    motherboard_2,
    motherboard_3,
    motherboard_4,
    motherboard_5,
    motherboard_6,
]


if __name__ == "__main__":
    for item in motherboard_db:
        print(item)
