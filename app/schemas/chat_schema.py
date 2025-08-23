from datetime import datetime
from typing import Any

from agents import TResponseInputItem
from pydantic import Field
from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.schemas.base import BaseDbModel


class ChatSchema(BaseDbModel):
    user_id: MongoObjectId
    config_id: MongoObjectId
    trace_id: str | None = None
    messages: list[TResponseInputItem] | list[Any] | None = None
    created_at: datetime = Field(default_factory=datetime.now)
