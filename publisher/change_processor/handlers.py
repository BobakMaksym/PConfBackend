from abc import ABC, abstractmethod
import logging
from typing import TYPE_CHECKING

from config import config as conf

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel

    from schemas import Change


logger = logging.getLogger(__name__)


class IChangeHandler(ABC):

    def __init__(
        self,
        channel: "BlockingChannel",
    ): ...

    @abstractmethod
    def handle(
        self,
        change: "Change",
    ): ...


class BaseOperationHandler(IChangeHandler):
    def __init__(self, channel: "BlockingChannel"):
        self._channel = channel

    @property
    def channel(self):
        return self._channel

    def handle(self, change: "Change"):
        msg = change.model_dump_json(exclude_none=True)
        self.channel.basic_publish(
            exchange=conf.RABBIT_EXCHANGE,
            routing_key=conf.RABBIT_ROUTING_KEY,
            body=msg,
        )

        logger.info(
            "Publish message to Q: operation=%r, coll=%r, id=%r; msg: %s",
            change.operation_type.value,
            change.ns.coll,
            str(change.id),
            msg,
        )


class DeleteHandler(BaseOperationHandler): ...


class UpdateHandler(BaseOperationHandler): ...


class InsertHandler(BaseOperationHandler): ...
