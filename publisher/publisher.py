from change_processor import (
    ChangeProcessor,
    DeleteHandler,
    InsertHandler,
    UpdateHandler,
    pipeline,
)
from config import config as conf, configure_logging, rabbit_connection_params
from enums import Operation
from mongo.db import Mongo

from rabbit import ComponentUpdateRabbit


configure_logging()


def main():

    mongo = Mongo(
        connection_str=conf.MONGO_CONNECTION_STRING,
        database=conf.MONGO_DATABASE,
        uuidRepresentation="standard",
    )

    with ComponentUpdateRabbit(connection_params=rabbit_connection_params) as rabbit:
        rabbit.create_queue()

        channel = rabbit.channel

        processor = ChangeProcessor(
            handlers={
                Operation.DELETE: DeleteHandler(channel=channel),
                Operation.UPDATE: UpdateHandler(channel=channel),
                Operation.INSERT: InsertHandler(channel=channel),
            }
        )

        mongo.watch_changes(processor=processor, pipeline=pipeline)


if __name__ == "__main__":
    main()
