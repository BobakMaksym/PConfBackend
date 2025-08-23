from pymongo.database import Database

from app.schemas.base import BaseDbModel as Component
from app.schemas.component_schema import (
    Cpu,
    Gpu,
    Ram,
    Motherboard,
    PowerSupply,
)


class BaseComponentRepo:
    model: Cpu = None
    collection: str = None
    mongo_search_index: str = None

    def __init__(self, db: Database):
        self.db = db["components"]
        self.col = db[self.collection]

    def find(self, filters: dict, limit: int) -> list[Component]:

        model = filters.pop("model", None)

        # aggregation pipeline with atlas search if `model` is passed
        if model:
            docs = self.col.aggregate(
                [
                    {
                        "$search": {
                            "index": self.mongo_search_index,
                            "text": {"query": model, "path": "model"},
                        }
                    },
                    {"$match": filters},
                    {"$limit": limit},
                ]
            )
        else:
            docs = self.col.find(filters).limit(limit)

        components = []
        for doc in docs:
            components.append(self.model(**doc))

        # print(components)

        return components


class CpuRepo(BaseComponentRepo):
    model = Cpu
    collection = "cpu"
    mongo_search_index = "cpu_search_index"


class GpuRepo(BaseComponentRepo):
    model = Gpu
    collection = "gpu"
    mongo_search_index = "gpu_search_index"


class RamRepo(BaseComponentRepo):
    model = Ram
    collection = "ram"


class MbRepo(BaseComponentRepo):
    model = Motherboard
    collection = "motherboard"


class PsuRepo(BaseComponentRepo):
    model = PowerSupply
    collection = "psu"
