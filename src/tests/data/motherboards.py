from src.domain.motherboard import MotherBoard


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


mb_asus_am4_ddr4_B550 = MotherBoard(
    model="ROG STRIX B550-F GAMING",
    manufacturer="ASUS",
    series="ROG",
    platform="AMD",
    socket="AM4",
    ram_type="DDR4",
    max_ram=128,
    chipset="B550",
)

mb_msi_lga1700_z690 = MotherBoard(
    model="MSI MPG Z690 EDGE WIFI",
    manufacturer="MSI",
    series="MPG",
    platform="Intel",
    socket="LGA1700",
    ram_type="DDR5",
    max_ram=128,
    chipset="Z690",
)

mb_gigabyte_am4_ddr4_B450 = MotherBoard(
    model="GIGABYTE B450M DS3H",
    manufacturer="GIGABYTE",
    series="Ultra Durable",
    platform="AMD",
    socket="AM4",
    ram_type="DDR4",
    max_ram=64,
    chipset="B450",
)

mb_asrock_lga1200_ddr4_Z590 = MotherBoard(
    model="ASROCK Z590 EXTREME",
    manufacturer="ASRock",
    series="Extreme",
    platform="Intel",
    socket="LGA1200",
    ram_type="DDR4",
    max_ram=128,
    chipset="Z590",
)

mb_aorus_am5_ddr5_X670E = MotherBoard(
    model="AORUS X670E MASTER",
    manufacturer="GIGABYTE",
    series="AORUS",
    platform="AMD",
    socket="AM5",
    ram_type="DDR5",
    max_ram=128,
    chipset="X670E",
)

mb_asus_lga1700_ddr5_Z790 = MotherBoard(
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
    mb_gigabyte_am5_ddr5_X870E,
    mb_asus_am4_ddr4_B550,
    mb_msi_lga1700_z690,
    mb_gigabyte_am4_ddr4_B450,
    mb_asrock_lga1200_ddr4_Z590,
    mb_aorus_am5_ddr5_X670E,
    mb_asus_lga1700_ddr5_Z790,
]


if __name__ == "__main__":
    for item in motherboard_db:
        print(item)
