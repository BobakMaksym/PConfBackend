import logging
from typesense.client import Client

from config import typesense_config, rabbit_connection_params, configure_logging
from enums import Operation
from index.index_repo import Index
from index.handlers import IndexDeleteHandler, IndexUpdateHandler, IndexInsertHandler
from index.processor import IndexChangeProcessor
from rabbit.component_updates import ComponentUpdateRabbit
from rabbit.consume_new_msg import ConsumeNewMessage


configure_logging()

logger = logging.getLogger(__name__)


def main():
    index_repo = Index(client=Client(config_dict=typesense_config))

    processor = IndexChangeProcessor(
        handlers={
            Operation.DELETE: IndexDeleteHandler(index_repo=index_repo),
            Operation.UPDATE: IndexUpdateHandler(index_repo=index_repo),
            Operation.INSERT: IndexInsertHandler(index_repo=index_repo),
        },
    )

    consume_new_message = ConsumeNewMessage(processor=processor)

    with ComponentUpdateRabbit(connection_params=rabbit_connection_params) as rabbit:
        rabbit.create_queue()

        rabbit.consume_messages(on_message_callback=consume_new_message)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
