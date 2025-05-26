from bson import ObjectId
from datetime import datetime
from typing import Literal

from app.helpers import COLLECTIONS
from app.models import (
    BaseComponentModel as Component,
    Build as BuildState,
)


# repositories/components.py
class ComponentRepo:
    def __init__(self, db, type_: COLLECTIONS):
        self.type_ = type_
        self.col = db[f"components.{self.type_}"]

    def find(self, filters: dict, *, limit: int = 20) -> list[Component]:
        q = {"in_stock": True, **filters}
        docs = self.col.find(q, projection={"specs": 1, "price": 1}).limit(limit)
        return [Component(**d) for d in docs]

    def by_id(self, _id: ObjectId) -> Component | None:
        doc = self.col.find_one({"_id": _id})
        return Component(**doc) if doc else None


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
