import json
from typing import TYPE_CHECKING
import logging

from typesense.client import Client

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties

from index.index_repo import Index
from rabbit.component_updates import ComponentUpdateRabbit
from index.handlers import IndexDeleteHandler, IndexUpdateHandler, IndexInsertHandler
from index.processor import IndexChangeProcessor
from enums import Operation
from schemas import Change

from config import typesense_config, rabbit_connection_params, configure_logging

configure_logging()

logger = logging.getLogger(__name__)


index_repo = Index(client=Client(config_dict=typesense_config))

processor = IndexChangeProcessor(
    handlers={
        Operation.DELETE: IndexDeleteHandler(index_repo=index_repo),
        Operation.UPDATE: IndexUpdateHandler(index_repo=index_repo),
        Operation.INSERT: IndexInsertHandler(index_repo=index_repo),
    },
)


def process_new_message(
    ch: "BlockingChannel",
    method: "Basic.Deliver",
    properties: "BasicProperties",
    body: bytes,
):
    decoded_body = body.decode()
    change = Change.model_validate_json(decoded_body)

    op_type, coll, id = change.operation_type.value, change.ns.coll, str(change.id)

    logger.info(
        "Start consuming new message from Q: operation=%r, coll=%r, id=%r; msg: %s",
        op_type,
        coll,
        id,
        decoded_body,
    )
    processor.process(change=change)

    logger.info(
        "Message processing completed: operation=%r, coll=%r, id=%r", op_type, coll, id
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


with ComponentUpdateRabbit(connection_params=rabbit_connection_params) as rabbit:
    rabbit.create_queue()

    rabbit.consume_messages(on_message_callback=process_new_message)
