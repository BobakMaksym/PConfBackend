from change_processor import (
    ChangeProcessor,
    DeleteHandler,
    InsertHandler,
    UpdateHandler,
    pipeline,
)
from config import config as conf, configure_logging
from enums import Operation
from mongo.db import Mongo


configure_logging()


mongo = Mongo(
    connection_str=conf.MONGO_CONNECTION_STRING,
    database=conf.MONGO_DATABASE,
    uuidRepresentation="standard",
)


processor = ChangeProcessor(
    handlers={
        Operation.DELETE: DeleteHandler(),
        Operation.UPDATE: UpdateHandler(),
        Operation.INSERT: InsertHandler(),
    },
)


mongo.watch_changes(
    processor=processor,
    pipeline=pipeline,
)
