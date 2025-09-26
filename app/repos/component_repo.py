from abc import ABC, abstractmethod
from typing import Any, Type, Iterable

from fastapi_filter.contrib.mongoengine import Filter

from app.documents.base import BaseComponentDocument
from app.documents import (
    CpuDocument,
    GpuDocument,
    MotherboardDocument,
    RamDocument,
    PsuDocument,
)
from app.schemas.base import BaseDbSchema
from app.schemas.component_schema import (
    CpuSchema,
    GpuSchema,
    RamSchema,
    MotherboardSchema,
    PowerSupplySchema,
)


class IComponentRepo(ABC):
    schema: Type[BaseDbSchema]
    collection: Type[BaseComponentDocument]

    @abstractmethod
    def __init__(self, db: Any = None): ...

    @abstractmethod
    def find(self, filters: Filter, limit: int) -> list[BaseDbSchema]: ...

    @abstractmethod
    def filter(
        self,
        filters: Filter,
        offset: int,
        limit: int,
        sort_by: Iterable[str] | None = None,
    ) -> list[BaseDbSchema]: ...

    @abstractmethod
    def count(self, filters: Filter) -> int: ...

    @abstractmethod
    def get_all(self) -> list[BaseDbSchema]: ...


class BaseComponentRepo(IComponentRepo):

    def __init__(self, db: Any = None):
        """the method is no longer needed"""
        pass

    def find(self, filters: Filter, limit: int):
        docs = filters.filter(self.collection.objects().limit(limit))  # type: ignore

        components = [self.schema.model_validate(doc) for doc in docs]

        return components

    def filter(
        self,
        filters: Filter,
        offset: int,
        limit: int,
        sort_by: Iterable[str] | None = None,
    ) -> list[BaseDbSchema]:
        cursor = self.collection.objects().skip(offset).limit(limit)  # type: ignore

        if sort_by:
            cursor = cursor.order_by(*sort_by)

        cursor = filters.filter(query=cursor)

        return [self.schema.model_validate(doc) for doc in cursor]

    def count(self, filters: Filter) -> int:
        count = filters.filter(self.collection.objects()).count()  # type: ignore
        return count

    def get_all(self):
        docs = self.collection.objects()  # type: ignore

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
