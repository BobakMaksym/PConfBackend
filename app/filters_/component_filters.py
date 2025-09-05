from app.documents import CpuDocument
from app.filters_.filter_utils import create_filter_class


CpuFilter = create_filter_class(
    model=CpuDocument,
    fields={
        "id": ["exact", "in"],
        "model": ["exact", "in", "contains"],
        "manufacturer": ["exact", "in"],
        "socket": ["exact", "in"],
        "ram_types": ["exact", "in", "contains"],
        "cores": ["exact", "gte", "lte"],
        "threads": ["exact", "gte", "lte"],
        "igp": ["exact"],
    },
)
