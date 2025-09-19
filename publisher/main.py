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
            Operation.DELETE: DeleteHandler(),
            Operation.UPDATE: UpdateHandler(),
            Operation.INSERT: InsertHandler(),
        },
        channel=channel,
    )

    mongo.watch_changes(processor=processor, pipeline=pipeline)
