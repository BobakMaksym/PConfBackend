from pydantic import BaseModel
from pydantic_extra_types.mongo_object_id import MongoObjectId


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: MongoObjectId = None
    exp: int = None
