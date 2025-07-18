from datetime import datetime
from typing import Any

from agents import TResponseInputItem
from pydantic import BaseModel, Field, model_validator

from app.schemas.pyobjectid import PyObjectId


class ChatSchema(BaseModel):
    id: PyObjectId = Field(alias="_id")
    user_id: PyObjectId
    config_id: PyObjectId
    trace_id: str | None = None
    messages: list[TResponseInputItem] | list[Any] | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            PyObjectId: lambda v: str(v),
        }
