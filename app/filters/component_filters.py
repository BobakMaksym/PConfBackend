from app.documents import (
    CpuDocument,
    GpuDocument,
    MotherboardDocument,
    PsuDocument,
    RamDocument,
    SsdDocument,
)
from app.filters.filter_utils import create_filter_class


EXACT = "exact"
IN = "in"
LTE = "lte"
GTE = "gte"

STR_SUFFIXES = (EXACT, IN)
INT_SUFFIXES = (EXACT, IN, LTE, GTE)
BOOL_SUFFIXES = (EXACT,)

id_model_manufacturer = {
    "id": STR_SUFFIXES,
    "model": (EXACT,),
    "manufacturer": STR_SUFFIXES,
}


CpuFilters = create_filter_class(
    model=CpuDocument,
    fields={
        **id_model_manufacturer,
        "socket": STR_SUFFIXES,
        "ram_types": STR_SUFFIXES,
        "cores": INT_SUFFIXES,
        "threads": INT_SUFFIXES,
        "igp": BOOL_SUFFIXES,
    },
)

GpuFilters = create_filter_class(
    model=GpuDocument,
    fields={
        **id_model_manufacturer,
        "model_gpu": STR_SUFFIXES,
        "memory_size": INT_SUFFIXES,
        "memory_type": STR_SUFFIXES,
        "monitors": INT_SUFFIXES,
        "power_consumption": INT_SUFFIXES,
        "additional_power": STR_SUFFIXES,
        "fans": INT_SUFFIXES,
        "lighting": BOOL_SUFFIXES,
    },
)

MotherboardFilters = create_filter_class(
    model=MotherboardDocument,
    fields={
        **id_model_manufacturer,
        "socket": STR_SUFFIXES,
        "form_factor": STR_SUFFIXES,
        "ram_type": STR_SUFFIXES,
        "ram_slots": INT_SUFFIXES,
        "m2_count": INT_SUFFIXES,
        "chipset": STR_SUFFIXES,
        "lighting": BOOL_SUFFIXES,
        "vrm_heatsink": BOOL_SUFFIXES,
        "wifi": BOOL_SUFFIXES,
    },
)

PsuFilters = create_filter_class(
    model=PsuDocument,
    fields={
        **id_model_manufacturer,
        "form_factor": STR_SUFFIXES,
        "power": INT_SUFFIXES,
        "mb_and_cpu_powersupply": STR_SUFFIXES,
        "efficiency": INT_SUFFIXES,
        "plus_12v": INT_SUFFIXES,
        "pci_e_8pin_6_2": INT_SUFFIXES,
        "pci_e_16pin": INT_SUFFIXES,
        "pci_e_6pin": INT_SUFFIXES,
        "pci_e_8pin": INT_SUFFIXES,
        "cable_system": STR_SUFFIXES,
        "certification": STR_SUFFIXES,
        "cooling_system": STR_SUFFIXES,
        "fan_bearing": STR_SUFFIXES,
        "manufacturers_warranty": INT_SUFFIXES,
        "dimensions": STR_SUFFIXES,
    },
)

RamFilters = create_filter_class(
    model=RamDocument,
    fields={
        **id_model_manufacturer,
        "type": STR_SUFFIXES,
        "modules": INT_SUFFIXES,
        "capacity": INT_SUFFIXES,
        "speed": INT_SUFFIXES,
        "cooling": BOOL_SUFFIXES,
        "colour": STR_SUFFIXES,
        "lighting": BOOL_SUFFIXES,
    },
)


SsdFilters = create_filter_class(
    model=SsdDocument,
    fields={
        **id_model_manufacturer,
        "form_factor": STR_SUFFIXES,
        "volume": INT_SUFFIXES,
        "read_speed": INT_SUFFIXES,
        "write_speed": INT_SUFFIXES,
        "controller": STR_SUFFIXES,
        "interface_m2": STR_SUFFIXES,
        "memory_type": STR_SUFFIXES,
        "nvme": BOOL_SUFFIXES,
        "radiator": BOOL_SUFFIXES,
    },
)
