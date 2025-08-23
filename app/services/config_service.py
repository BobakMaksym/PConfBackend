from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.helpers import COLLECTIONS
from app.repos import config_repo


COMPONENT_COUNT = 500


class ConfigService:

    @staticmethod
    def create(user_id: MongoObjectId) -> MongoObjectId:
        """create a new build in the db"""

        build_id = config_repo.create(user_id)
        return build_id

    @staticmethod
    def get(build_id: MongoObjectId):
        """Get the current state of the PC config"""

        build = config_repo.get_full_build(build_id)

        return build

    @staticmethod
    def delete(build_id: MongoObjectId):
        config_repo.delete(build_id=build_id)

    @staticmethod
    def add_component(build_id: MongoObjectId, component: COLLECTIONS, component_id):
        """Adds a components to the PC config"""

        config_repo.add_component(build_id, component, component_id)

        build = config_repo.get_full_build(build_id)

        return build

    @staticmethod
    def remove_component(build_id: MongoObjectId, type_: COLLECTIONS):
        """removes a component from the assembly"""
        build = config_repo.get_config(build_id)
        if not build:
            raise ValueError("Unknown build")

        config_repo.col.update_one({"_id": build_id}, {"$unset": {type_: 1}})
