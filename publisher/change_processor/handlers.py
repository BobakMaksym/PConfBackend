import logging
from typing import TYPE_CHECKING

from interfaces import IChangeHandler

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel

    from schemas import Change


logger = logging.getLogger(__name__)


def test_log(change: "Change"):

    message = change.model_dump_json()

    # rabbit.publish_message(message)

    logger.info("\n%s", message)


def produce_message(message: "Change", channel: "BlockingChannel"):
    msg = message.model_dump_json()
    channel.basic_publish(
        exchange="",
        routing_key="components",
        body=msg,
    )


class DeleteHandler(IChangeHandler):

    def handle(self, change: "Change", channel: "BlockingChannel"):
        id, coll = change.id, change.ns.coll

        produce_message(message=change, channel=channel)
        test_log(change)

        pass


class UpdateHandler(IChangeHandler):

    def handle(self, change: "Change", channel: "BlockingChannel"):
        id, coll = change.id, change.ns.coll

        produce_message(message=change, channel=channel)
        test_log(change)

        pass


class InsertHandler(IChangeHandler):

    def handle(self, change: "Change", channel: "BlockingChannel"):
        id, coll = change.id, change.ns.coll

        produce_message(message=change, channel=channel)
        test_log(change)

        pass
