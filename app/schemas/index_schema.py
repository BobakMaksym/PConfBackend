from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from pydantic_extra_types.mongo_object_id import MongoObjectId


class IndexSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=True,
    )

    id: MongoObjectId = Field(
        validation_alias=AliasChoices("id", "_id"),
        serialization_alias="id",
    )
    model: str
