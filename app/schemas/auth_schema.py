from pydantic import BaseModel
from pydantic_extra_types.mongo_object_id import MongoObjectId


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayloadSchema(BaseModel):
    sub: MongoObjectId = None
    exp: int = None
