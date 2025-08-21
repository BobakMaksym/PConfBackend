from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from pydantic_extra_types.mongo_object_id import MongoObjectId


class BaseDbModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    id: MongoObjectId | None = Field(
        validation_alias=AliasChoices("id", "_id"),
        serialization_alias="id",
        default=None,
    )
