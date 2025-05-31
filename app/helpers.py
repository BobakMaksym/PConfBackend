import json
from typing import Any, Literal, Mapping

from pydantic import BaseModel

COLLECTIONS = Literal["cpu", "gpu", "motherboard", "psu", "ram"]


def normalize_filters(filters: BaseModel) -> dict[str, Any]:
    raw_filters = filters.model_dump(exclude_none=True, by_alias=True)
    str_filters = json.dumps(raw_filters).lower()
    parsed_filters = json.loads(str_filters)

    return parsed_filters


if __name__ == "__main__":
    from pydantic import Field

    class IntRange(BaseModel):
        gt: int | None = Field(alias="$gt", default=None)
        lt: int | None = Field(alias="$lt", default=None)

    class In(BaseModel):
        in_: list[str] = Field(alias="$in", default=None)

    class CpuFilters(BaseModel):
        manufacturer: str | In | None = None
        socket: str | In | None = None
        cores: int | IntRange | None = None
        info: dict[str, Any] | None = None

    filters = CpuFilters(
        cores={"$gt": 6, "$lt": 12},
        manufacturer={"$in": ["INTEL", "aMD"]},
        info={"DESCRIPTION": "SOME TEXT"},
    )
    filters_norm = normalize_filters(filters)
    print(filters_norm)

    filters = CpuFilters(
        cores={"$gt": 6, "$lt": 12},
        manufacturer="INTEL",
    )
    filters_norm = normalize_filters(filters)
    print(filters_norm)


# def to_lowercase_values(obj):
#     """
#     Проходить рекурсивно по dict / list / tuple / set і
#     перетворює **лише рядкові значення** на lower().
#     Ключі залишають як є, щоби не ламати $оператори та назви полів.
#     """
#     if isinstance(obj, str):
#         return obj.lower()

#     # Для ітерованих структур – обробляємо кожен елемент
#     if isinstance(obj, Mapping):
#         return {k: to_lowercase_values(v) for k, v in obj.items()}

#     if isinstance(obj, (list, tuple, set)):
#         t = type(obj)
#         return t(to_lowercase_values(x) for x in obj)

#     # Інші типи (int, bool, None, ...) лишаємо без змін
#     return obj
