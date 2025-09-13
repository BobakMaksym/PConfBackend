from typing import Literal

from app.schemas.change_stream_schema import ChangeStreamSchema, op_types
from app.indexer.interface import IChangeHandler


class ChangeStreamProcessor:
    def __init__(self, handlers: dict[op_types, IChangeHandler]):
        self.handlers = handlers

    def process(self, change: ChangeStreamSchema):
        handler = self.handlers.get(change.operation_type)
        if handler:
            handler.handle(change)
