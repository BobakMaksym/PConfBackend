from typing import Any, Literal

from bson import ObjectId
from pydantic import BaseModel, computed_field, Field
from pydantic_extra_types.mongo_object_id import MongoObjectId


class Namespace(BaseModel):
    db: str
    coll: str


op_types = Literal["insert", "update", "delete"]


class ChangeStreamSchema(BaseModel):
    document_key: dict[str, MongoObjectId] = Field(validation_alias="documentKey")
    operation_type: op_types = Field(validation_alias="operationType")
    ns: Namespace

    # Поля для різних типів операцій
    full_document: dict[str, Any] | None = Field(
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

    pprint(ChangeStreamSchema(**insert_doc))
    pprint(ChangeStreamSchema(**update_doc))
    pprint(ChangeStreamSchema(**delete_doc))
