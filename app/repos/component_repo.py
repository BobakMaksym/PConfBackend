from pymongo.database import Database

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


class BaseComponentRepo:
    schema: CpuSchema = None
    collection: CpuDocument = None
    mongo_search_index: str = None

    def __init__(self, db: Database):
        """the method is no longer needed"""
        pass

    def find(self, filters: dict, limit: int) -> list[Component]:

        component_model = filters.pop("model", None)

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
            docs = self.collection.objects(**filters).limit(limit)

        components = [self.schema.model_validate(doc) for doc in docs]

        return components


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
