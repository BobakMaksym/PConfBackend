from abc import ABC, abstractmethod
from typing import Any, ClassVar

from app.db import db
from app.helpers import COLLECTIONS
from app.schemas.pyobjectid import PyObjectId
from app.schemas.component_schema import Build
from app.repo import BuildRepo


COMPONENT_COUNT = 500


class ConfigService:

    @staticmethod
    def create(user_id: PyObjectId) -> PyObjectId:
        """create a new build in the db"""

        build_id = BuildRepo(db).create(user_id)
        return build_id

    @staticmethod
    def get(build_id: PyObjectId):
        """Get the current state of the PC config"""

        _build = BuildRepo(db).get_full_build(build_id)

        build = Build(**_build)

        return build

    @staticmethod
    def delete(build_id: PyObjectId):
        BuildRepo(db).delete(build_id=build_id)

    @staticmethod
    def add_component(build_id: PyObjectId, component: COLLECTIONS, component_id):
        """Adds a components to the PC config"""

        BuildRepo(db).add_component(build_id, component, component_id)

        build = BuildRepo(db).get_full_build(build_id)

        return Build(**build)

    @staticmethod
    def remove_component(build_id: PyObjectId, type_: COLLECTIONS):
        """removes a component from the assembly"""
        build = BuildRepo(db).get_config(build_id)
        if not build:
            raise ValueError("Unknown build")

        BuildRepo(db).col.update_one({"_id": build_id}, {"$unset": {type_: 1}})
