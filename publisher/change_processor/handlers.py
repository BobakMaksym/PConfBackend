import logging
from typing import TYPE_CHECKING

from config import config as conf
from interfaces import IChangeHandler

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


class DeleteHandler(IChangeHandler):

    def handle(self, change: "Change", channel: "BlockingChannel"):
        id, coll = change.id, change.ns.coll

        produce_message(message=change, channel=channel)

        pass


class UpdateHandler(IChangeHandler):

    def handle(self, change: "Change", channel: "BlockingChannel"):
        id, coll = change.id, change.ns.coll

        produce_message(message=change, channel=channel)

        pass


class InsertHandler(IChangeHandler):

    def handle(self, change: "Change", channel: "BlockingChannel"):
        id, coll = change.id, change.ns.coll

        produce_message(message=change, channel=channel)

        pass
