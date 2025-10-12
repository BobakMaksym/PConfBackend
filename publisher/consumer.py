import asyncio
import logging

from typesense.client import Client

from config import typesense_config, config as conf, configure_logging
from enums import Operation
from index.index_repo import Index
from index.handlers import IndexDeleteHandler, IndexUpdateHandler, IndexInsertHandler
from index.processor import IndexChangeProcessor
from rabbit.asyncio_rabbit import AsyncioRabbit


configure_logging()

logger = logging.getLogger(__name__)


async def main():
    index_repo = Index(client=Client(config_dict=typesense_config))

    processor = IndexChangeProcessor(
        handlers={
            Operation.DELETE: IndexDeleteHandler(index_repo=index_repo),
            Operation.UPDATE: IndexUpdateHandler(index_repo=index_repo),
            Operation.INSERT: IndexInsertHandler(index_repo=index_repo),
        },
    )
    async with AsyncioRabbit(conf.RABBIT_CONNECTION_STR_ASYNC) as rabbit:
        rabbit.set_message_processor(processor=processor)
        await rabbit.consume_messages()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit(0)
