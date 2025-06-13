from datetime import datetime
from typing import Literal

from pymongo.collection import Collection
from pymongo.database import Database

from app.helpers import COLLECTIONS
from app.schemas.pyobjectid import PyObjectId
from app.schemas.component_schema import (
    BaseComponentModel as Component,
    Build,
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

    def create(self, user_id: PyObjectId | None = None) -> Build:
        build = Build(user=user_id)
        res = self.col.insert_one(build.model_dump())

        return res.inserted_id

    def load(self, build_id: PyObjectId) -> Build | None:
        doc = self.col.find_one({"_id": build_id})

        return doc if doc else None

    def add_component(
        self,
        build_id: PyObjectId,
        component_type: COLLECTIONS,
        component_id: PyObjectId,
    ):
        build = self.load(build_id)
        # print(f"\nBUILD: {build}\n", flush=True)
        if not build:
            raise ValueError("Unknown build")

        self.col.update_one(
            {"_id": build_id},
            {"$set": {component_type: component_id}},
        )

    def get_full_build(self, _id: PyObjectId):
        components = ["cpu", "gpu", "motherboard", "ram", "psu"]

        pipeline = []
        match_stage = {"$match": {"_id": _id}}
        lookup_stages = []
        set_stage = {
            "$set": {c: {"$arrayElemAt": [f"${c}_full", 0]} for c in components}
        }
        unset_stage = {"$unset": [f"{c}_full" for c in components]}

        for component in components:
            lookup_stages.append(
                {
                    "$lookup": {
                        "from": component,
                        "localField": component,
                        "foreignField": "_id",
                        "as": f"{component}_full",
                    }
                }
            )
        pipeline.append(match_stage)
        pipeline.extend(lookup_stages)
        pipeline.append(set_stage)
        pipeline.append(unset_stage)

        # from pprint import pprint
        # pprint(pipeline)

        cursor = self.col.aggregate(pipeline)
        build = list(cursor)[0]

        return build

    # def save_state(self, build_id: PyObjectId, state: dict):
    #     # self.col.update_one(
    #     #     {"_id": build_id},
    #     #     {"$set": {"state": state, "updated_at": datetime.now()}},
    #     # )

    #     print(f"\nSAVE STATE: {state}\n", flush=True)

    #     self.col.update_one(
    #         {"_id": build_id},
    #         state,
    #         # {"$set": {"state": state, "updated_at": datetime.now()}},
    #     )


# class ChatRepo:

#     def __init__(self, db):
#         self.col: Collection = db["chats"]

#     def create(self, user_id: PyObjectId) -> PyObjectId:
#         chat = Chat(user_id=user_id).model_dump(by_alias=True)
#         res = self.col.insert_one(chat)
#         return res.inserted_id

#     def delete(self, chat_id: PyObjectId):
#         return self.col.delete_one({"_id": chat_id})
