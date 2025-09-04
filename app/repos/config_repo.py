import logging

from pymongo.collection import Collection
from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.helpers import COLLECTIONS
from app.schemas.pc_config_schema import PcConfigSchema, PcComponentsId


logger = logging.getLogger("app")


class ConfigRepo:
    def __init__(self, db):
        self.col: Collection = db["builds"]

    def create(self, user_id: MongoObjectId) -> MongoObjectId:
        build = PcConfigSchema(user_id=user_id)
        res = self.col.insert_one(build.model_dump_for_db())

        return res.inserted_id

    def delete(self, build_id: MongoObjectId):
        self.col.delete_one({"_id": build_id})

    def load(self, build_id: MongoObjectId) -> PcConfigSchema | None:
        """deprecated, use `get_config`"""

        doc = self.col.find_one({"_id": build_id})

        return doc if doc else None

    def get_config(self, config_id: MongoObjectId) -> PcComponentsId | None:
        config = self.col.find_one({"_id": config_id})
        if not config:
            return None
        return PcComponentsId(**config)

    def get_config_errors(self, config_id: MongoObjectId) -> PcConfigSchema | None:
        errors = self.col.find_one({"_id": config_id}, {"errors": 1})

        return errors

    def add_component(
        self,
        build_id: MongoObjectId,
        component_type: COLLECTIONS,
        component_id: MongoObjectId,
    ):
        build = self.load(build_id)

        if not build:
            raise ValueError("Unknown build")

        self.col.update_one(
            {"_id": build_id},
            {"$set": {component_type: component_id}},
        )
        logger.debug(
            "add_component: in config %s add %s %s",
            build_id,
            component_type,
            component_id,
        )

    def get_full_build(self, _id: MongoObjectId):
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

        cursor = self.col.aggregate(pipeline)

        build = list(cursor)
        if not build:
            return None

        return PcConfigSchema(**build[0])
