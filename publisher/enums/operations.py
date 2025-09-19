from enum import StrEnum

from enums.mixin import ValuesMixin


class Operation(ValuesMixin, StrEnum):
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
