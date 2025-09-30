from pydantic import BaseModel, Field, computed_field, ConfigDict
from pydantic_extra_types.mongo_object_id import MongoObjectId


class Document(BaseModel):
    model_config = ConfigDict(extra="allow")

    # id: MongoObjectId
    model: str


class Hit(BaseModel):
    document: Document


class RequestParams(BaseModel):
    collection_name: str
    first_q: str
    per_page: int
    q: str


class SearchResultSchema(BaseModel):
    found: int
    out_of: int
    page: int
    request_params: RequestParams

    hits_raw: list[Hit] = Field(alias="hits", exclude=True)

    @computed_field
    def hits(self) -> list[Document]:
        return [hit.document for hit in self.hits_raw]
