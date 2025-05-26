from bson import ObjectId
from datetime import datetime
from typing import Literal

from pymongo.collection import Collection
from pymongo.database import Database

from app.helpers import COLLECTIONS
from app.models import (
    BaseComponentModel as Component,
    Build as BuildState,
    Cpu,
    Gpu,
)


class BaseComponentRepo:
    model: Cpu = None
    collection: str = None

    def __init__(self, db: Database):
        self.db = db["components"]
        self.col = db[self.collection]

    def find(self, filters: dict, limit: int) -> list[Component]:
        docs = self.col.find(filters).limit(limit)

        components = []
        for doc in docs:
            components.append(self.model(**doc))

        print(components)

        return components


class CpuRepo(BaseComponentRepo):
    model = Cpu
    collection = "cpu"


class GpuRepo(BaseComponentRepo):
    model = Gpu
    collection = "gpu"


# repositories/builds.py
class BuildRepo:
    def __init__(self, db):
        self.col = db["builds"]

    def create(self, user_id: ObjectId | None) -> BuildState:
        res = self.col.insert_one(
            {
                "user_id": user_id,
                "state": {},
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        )
        return BuildState(id=res.inserted_id, state={})

    def load(self, build_id: ObjectId) -> BuildState | None:
        doc = self.col.find_one({"_id": build_id})
        return BuildState.model_validate(doc) if doc else None

    def save_state(self, build_id: ObjectId, state: dict):
        self.col.update_one(
            {"_id": build_id},
            {"$set": {"state": state, "updated_at": datetime.now()}},
        )
