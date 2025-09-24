from abc import ABC, abstractmethod
from typing import Any

from fastapi_filter.contrib.mongoengine import Filter

from app.documents import (
    CpuDocument,
    GpuDocument,
    MotherboardDocument,
    RamDocument,
    PsuDocument,
)
from app.schemas.base import BaseDbSchema as Component
from app.schemas.component_schema import (
    CpuSchema,
    GpuSchema,
    RamSchema,
    MotherboardSchema,
    PowerSupplySchema,
)


class IComponentRepo(ABC):
    schema: CpuSchema
    collection: CpuDocument

    @abstractmethod
    def __init__(self, db: Any = None): ...

    @abstractmethod
    def find(self, filters: Filter, limit: int) -> list[Component]: ...

    @abstractmethod
    def get_all(self) -> list[Component]: ...


class BaseComponentRepo(IComponentRepo):
    schema: CpuSchema
    collection: CpuDocument

    def __init__(self, db: Any = None):
        """the method is no longer needed"""
        pass

    def find(self, filters: Filter, limit: int) -> list[Component]:
        docs = filters.filter(self.collection.objects().limit(limit))

        components = [self.schema.model_validate(doc) for doc in docs]

        return components

    def get_all(self):
        docs = self.collection.objects()

        return [self.schema.model_validate(doc) for doc in docs]


class CpuRepo(BaseComponentRepo):
    schema = CpuSchema
    collection = CpuDocument


class GpuRepo(BaseComponentRepo):
    schema = GpuSchema
    collection = GpuDocument


class RamRepo(BaseComponentRepo):
    schema = RamSchema
    collection = RamDocument


class MbRepo(BaseComponentRepo):
    schema = MotherboardSchema
    collection = MotherboardDocument


class PsuRepo(BaseComponentRepo):
    schema = PowerSupplySchema
    collection = PsuDocument


repos = {
    "cpu": CpuRepo,
    "ram": RamRepo,
    "gpu": GpuRepo,
    "psu": PsuRepo,
    "motherboard": MbRepo,
}

component_repos = repos
