from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, model_validator

from app.schemas.pyobjectid import PyObjectId


class ChatSchema(BaseModel):
    id: PyObjectId = Field(alias="_id")
    user_id: PyObjectId
    config_id: PyObjectId

    messages: list[str | None] | list[dict[str, Any] | None] = Field(
        default_factory=list
    )

    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            PyObjectId: lambda v: str(v),
        }
