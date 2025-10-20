from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from pydantic_extra_types.mongo_object_id import MongoObjectId


class BaseDbSchema(BaseModel):
    """
    Basic model for working with objects from the database
    """

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    id: MongoObjectId = Field(
        validation_alias=AliasChoices("id", "_id"), serialization_alias="id"
    )

    def model_dump_for_db(self, *args, **kwargs):
        """
        Returns a dictionary ready for insertion into the database.
        The method replaces `id` with `_id`,
        """

        data = self.model_dump(*args, **kwargs)
        id = data.pop("id", None)
        if id:
            data["_id"] = id
        return data
