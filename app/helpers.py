from typing import Any, Literal

COLLECTIONS = Literal["cpu", "gpu", "motherboard", "psu", "ram"]


def normalize_filters(filters: dict) -> dict[str, Any]:
    _filters_norm = {}

    for k, v in filters.items():
        if v == None:
            continue
        elif isinstance(v, str):
            _filters_norm[k] = v.lower()
        else:
            _filters_norm[k] = v
    return _filters_norm
