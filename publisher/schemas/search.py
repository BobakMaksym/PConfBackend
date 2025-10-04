from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from pydantic_extra_types.mongo_object_id import MongoObjectId


class IndexDoc(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=True,
        extra="allow",
    )

    id: MongoObjectId = Field(
        validation_alias=AliasChoices("id", "_id"),
        serialization_alias="id",
    )
    model: str | None = None


if __name__ == "__main__":
    from bson import ObjectId

    m = IndexDoc(_id=ObjectId(), model="amd r5 3600")  # type: ignore
    print(m)
    print(m.model_dump_json())
    print(type(m.model_dump_json()))
    print(m.model_dump(mode="json"))
