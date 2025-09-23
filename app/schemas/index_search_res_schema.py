from pydantic import BaseModel, ConfigDict, Field, computed_field
from pydantic_extra_types.mongo_object_id import MongoObjectId


class Hit(BaseModel):
    document: dict[str, MongoObjectId | str]


class SearchResultSchema(BaseModel):
    model_config = ConfigDict()

    found: int
    out_of: int
    page: int
    hits_raw: list[Hit] = Field(alias="hits", exclude=True)

    @computed_field
    def hits(self) -> list[dict[str, MongoObjectId | str]]:
        return [hit.document for hit in self.hits_raw]
