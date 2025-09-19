from enum import StrEnum

from enums.mixin import ValuesMixin


class Collection(ValuesMixin, StrEnum):
    CPU = "cpu"
    GPU = "gpu"
    RAM = "ram"
    PSU = "psu"
    MOTHERBOARD = "motherboard"
