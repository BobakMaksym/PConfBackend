from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties

    from index.processor import IIndexChangeProcessor

from schemas import Change


logger = logging.getLogger(__name__)


class ConsumeNewMessage:
    """Callable class for consume and process messages from RabbitMQ.

    The main idea: to avoid using hard-coded dependencies.

    The class helps:
    - inject `processor` without global variables;
    - easier to test, mock, and extend;
    """

    def __init__(self, processor: "IIndexChangeProcessor"):
        self.processor = processor

    def __call__(
        self,
        ch: "BlockingChannel",
        method: "Basic.Deliver",
        properties: "BasicProperties",
        body: bytes,
    ):
        decoded_body = body.decode()
        change = Change.model_validate_json(decoded_body)

        op_type, coll, id = change.operation_type.value, change.ns.coll, str(change.id)
        log = (
            "Start consuming new message from Q: operation=%r, coll=%r, id=%r; msg: %s"
        )
        logger.info(log, op_type, coll, id, decoded_body)

        self.processor.process(change=change)

        log = "Message processing completed: operation=%r, coll=%r, id=%r"
        logger.info(log, op_type, coll, id)

        ch.basic_ack(delivery_tag=method.delivery_tag)  # type: ignore
