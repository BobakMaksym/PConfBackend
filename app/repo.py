from typing import Any
from agents import trace
from pymongo.collection import Collection
from pymongo.database import Database

from app.core import exceptions as e
from app.core.config import settings
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
from app.schemas.chat_schema import ChatSchema
from app.prompt import messages


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


# repositories/builds.py
class BuildRepo:
    def __init__(self, db):
        self.col: Collection = db["builds"]

    def create(self, user_id: PyObjectId) -> PyObjectId:
        build = Build(user_id=user_id)
        res = self.col.insert_one(build.model_dump())

        return res.inserted_id

    def delete(self, build_id: PyObjectId):
        self.col.delete_one({"_id": build_id})

    def load(self, build_id: PyObjectId) -> Build | None:
        """deprecated, use `get_config`"""

        doc = self.col.find_one({"_id": build_id})

        return doc if doc else None

    def get_config(self, config_id: PyObjectId) -> Build | None:
        return self.col.find_one({"_id": config_id})

    def get_config_errors(self, config_id: PyObjectId) -> Build | None:
        errors = self.col.find_one({"_id": config_id}, {"errors": 1})

        return errors

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


class ChatRepo:

    def __init__(self, db):
        self.col: Collection = db["chats"]

    def create(self, user_id: PyObjectId, config_id: PyObjectId) -> ChatSchema:
        chat = ChatSchema(
            _id=config_id,
            config_id=config_id,
            user_id=user_id,
            trace_id=trace(settings.WORKFLOW_NAME).trace_id,
            messages=[{"role": "assistant", "content": messages.START_MESSAGE}],
        )
        res = self.col.insert_one(chat.model_dump(by_alias=True))
        chat.id = res.inserted_id

        return chat

    def delete(self, chat_id: PyObjectId):
        return self.col.delete_one({"_id": chat_id})

    def get_user_chat(self, user_id: PyObjectId):
        _chats = self.col.find({"user_id": user_id}, {"messages": 0})

        chats = []
        for chat in _chats:
            chat = ChatSchema(**chat).model_dump(exclude_none=True)
            chats.append(chat)

        return chats

    def get_chat(self, chat_id: PyObjectId):
        _chat = self.col.find_one({"_id": chat_id})
        chat = ChatSchema(**_chat)
        messages = []
        for msg in chat.messages:
            msg_type = msg.get("type")
            if msg_type in ("message", None):
                messages.append(msg)
        chat.messages = messages
        # chat.messages = [
        #     msg for msg in chat.messages if msg.get("type") in ("message", None)
        # ]
        return chat.model_dump(by_alias=True)

    def update_history(self, chat_id: PyObjectId, message: str):
        """просто додати повідомлення"""

        result = self.col.find_one_and_update(
            {"_id": chat_id},
            {"$push": {"messages": message}},
        )
        if not result:
            raise e.DocumentDoesNotExist
        return result
