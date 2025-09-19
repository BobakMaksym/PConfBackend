from typing import Any

from pydantic import BaseModel, computed_field, Field
from pydantic_extra_types.mongo_object_id import MongoObjectId

from enums import Operation


class Namespace(BaseModel):
    db: str
    coll: str


class Change(BaseModel):
    document_key: dict[str, MongoObjectId] = Field(validation_alias="documentKey")
    operation_type: Operation = Field(validation_alias="operationType")
    ns: Namespace

    # Поля для різних типів операцій
    full_document: dict[str, MongoObjectId | Any] | None = Field(
        default=None, validation_alias="fullDocument"
    )
    update_description: dict[str, Any] | None = Field(
        default=None, validation_alias="updateDescription"
    )

    @computed_field
    @property
    def id(self) -> MongoObjectId:
        return self.document_key["_id"]


if __name__ == "__main__":

    # TEST

    from bson import ObjectId

    insert_doc = {
        "operationType": "insert",
        "fullDocument": {"_id": ObjectId(), "name": "max"},
        "ns": {"db": "components", "coll": "users"},
        "documentKey": {"_id": ObjectId()},
    }

    update_doc = {
        "operationType": "update",
        "ns": {"db": "components", "coll": "users"},
        "documentKey": {"_id": ObjectId()},
        "updateDescription": {
            "updatedFields": {"name": "1max"},
            "removedFields": [],
            "truncatedArrays": [],
        },
    }

    delete_doc = {
        "operationType": "delete",
        "ns": {"db": "components", "coll": "users"},
        "documentKey": {"_id": ObjectId()},
    }

    pprint = lambda data: print(f"\n{repr(data)}")

    pprint(Change(**insert_doc))
    pprint(Change(**update_doc))
    pprint(Change(**delete_doc))
