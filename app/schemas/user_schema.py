from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic_extra_types.mongo_object_id import MongoObjectId


class UserAuth(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    email: EmailStr = Field(..., description="user email")
    username: str = Field(..., min_length=5, max_length=50, description="user username")
    password: str = Field(..., min_length=5, max_length=24, description="user password")


class UserOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # id: MongoObjectId = Field(alias="_id", serialization_alias="id")
    user_id: UUID
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = False


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
