from abc import ABC, abstractmethod

from pymongo.database import Database

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
    mongo_search_index: str

    @abstractmethod
    def find(self, filters: Filter, limit: int) -> list[Component]: ...

    @abstractmethod
    def get_all(self) -> list[Component]: ...


class BaseComponentRepo(IComponentRepo):
    schema: CpuSchema
    collection: CpuDocument
    mongo_search_index: str

    def __init__(self, db: Database):
        """the method is no longer needed"""
        pass

    def find(self, filters: Filter, limit: int) -> list[Component]:

        # component_model = filters.pop("model", None)
        component_model = None

        docs = []

        # aggregation pipeline with atlas search if `model` is passed
        if component_model:
            pipeline = [
                {
                    "$search": {
                        "index": self.mongo_search_index,
                        "text": {"query": component_model, "path": "model"},
                    }
                },
                {"$match": filters},
                {"$limit": limit},
            ]
            docs = self.collection.objects().aggregate(pipeline)

        else:
            docs = filters.filter(self.collection.objects().limit(limit))

        components = [self.schema.model_validate(doc) for doc in docs]

        return components

    def get_all(self):
        docs = self.collection.objects()

        return [self.schema.model_validate(doc) for doc in docs]


class CpuRepo(BaseComponentRepo):
    schema = CpuSchema
    collection = CpuDocument
    mongo_search_index = "cpu_search_index"


class GpuRepo(BaseComponentRepo):
    schema = GpuSchema
    collection = GpuDocument
    mongo_search_index = "gpu_search_index"


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
