from abc import ABC, abstractmethod
import logging
from typing import TYPE_CHECKING

from config import config as conf

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel

    from schemas import Change


logger = logging.getLogger(__name__)


def produce_message(message: "Change", channel: "BlockingChannel"):
    msg = message.model_dump_json()
    channel.basic_publish(
        exchange=conf.RABBIT_EXCHANGE,
        routing_key=conf.RABBIT_ROUTING_KEY,
        body=msg,
    )

    logger.info(
        "Publish to Q: operation=%r, coll=%r, id=%r",
        message.operation_type.value,
        message.ns.coll,
        str(message.id),
    )


class IChangeHandler(ABC):

    @abstractmethod
    def handle(
        self,
        change: "Change",
        channel: "BlockingChannel",
    ): ...


class DeleteHandler(IChangeHandler):

    def handle(self, change: "Change", channel: "BlockingChannel"):
        produce_message(message=change, channel=channel)


class UpdateHandler(IChangeHandler):

    def handle(self, change: "Change", channel: "BlockingChannel"):
        produce_message(message=change, channel=channel)


class InsertHandler(IChangeHandler):

    def handle(self, change: "Change", channel: "BlockingChannel"):
        produce_message(message=change, channel=channel)
