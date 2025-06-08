from datetime import datetime
from typing import Literal

from pymongo.collection import Collection
from pymongo.database import Database

from app.helpers import COLLECTIONS
from app.schemas.pyobjectid import PyObjectId
from app.schemas.component_schema import (
    BaseComponentModel as Component,
    Build as BuildState,
    Cpu,
    Gpu,
    Ram,
    Motherboard,
    PowerSupply,
)
from app.schemas.chat_schema import Chat


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

        print(components)

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


# repositories/builds.py
class BuildRepo:
    def __init__(self, db):
        self.col: Collection = db["builds"]

    def create(self, user_id: PyObjectId | None = None) -> BuildState:
        res = self.col.insert_one(
            {
                # "user_id": user_id,
                # "state": {},
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        )
        return BuildState(id=res.inserted_id)

    def load(self, build_id: PyObjectId) -> BuildState | None:
        doc = self.col.find_one({"_id": build_id})
        return BuildState.model_validate(doc) if doc else None

    def add_component(
        self,
        build_id: PyObjectId,
        component_type: COLLECTIONS,
        component_id: PyObjectId,
    ):
        build = self.load(build_id)
        if not build:
            raise ValueError("Unknown build")

        build.state[component_type] = component_id
        self.save_state(build_id, build.state)

    # def save_state(self, build_id: PyObjectId, state: dict):
    #     self.col.update_one(
    #         {"_id": build_id},
    #         {"$set": {"state": state, "updated_at": datetime.now()}},
    #     )


class ChatRepo:

    def __init__(self, db):
        self.col: Collection = db["chats"]

    def create(self, user_id: PyObjectId) -> PyObjectId:
        chat = Chat(user_id=user_id).model_dump(by_alias=True)
        res = self.col.insert_one(chat)
        return res.inserted_id

    def delete(self, chat_id: PyObjectId):
        return self.col.delete_one({"_id": chat_id})
