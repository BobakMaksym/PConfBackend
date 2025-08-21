from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import BaseDbModel


class UserAuth(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    email: EmailStr = Field(..., description="user email")
    username: str = Field(..., min_length=5, max_length=50, description="user username")
    password: str = Field(..., min_length=5, max_length=24, description="user password")


class UserOut(BaseDbModel):
    user_id: UUID
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = False


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class User(BaseDbModel):
    user_id: UUID
    username: str
    email: EmailStr
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = False
