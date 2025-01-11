from enum import Enum


class ComponentType(str, Enum):
    cpu = "cpu"
    gpu = "gpu"
    ram = "ram"
    pcu = "pcu"
    mother_board = "mother board"
