import asyncio

from change_processor import (
    ChangeProcessor,
    DeleteHandler,
    InsertHandler,
    UpdateHandler,
    pipeline,
)
from config import config as conf, configure_logging
from enums import Operation
from mongo.db_async import AsyncMongo


configure_logging()


from rabbit.asyncio_rabbit import AsyncioRabbit


async def main():

    async with AsyncioRabbit(conf.RABBIT_CONNECTION_STR_ASYNC) as rabbit:
        mongo = AsyncMongo(
            connection_str=conf.MONGO_CONNECTION_STRING,
            database=conf.MONGO_DATABASE,
        )
        processor = ChangeProcessor(
            handlers={
                Operation.DELETE: DeleteHandler(broker=rabbit),
                Operation.UPDATE: UpdateHandler(broker=rabbit),
                Operation.INSERT: InsertHandler(broker=rabbit),
            }
        )

        await mongo.watch_changes(processor, pipeline)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit(0)
