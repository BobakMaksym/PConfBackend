from typing import TYPE_CHECKING

from pymongo import MongoClient

if TYPE_CHECKING:
    from pymongo.database import Database
    from pymongo.typings import _Pipeline

    from change_processor import IChangeProcessor

from schemas import Change


class Mongo:

    def __init__(self, connection_str: str, database: str, **kwargs):
        self._client = MongoClient(host=connection_str, **kwargs)
        self._database: "Database" = self._client[database]

    @property
    def database(self) -> "Database":
        return self._database

    @property
    def client(self) -> MongoClient:
        return self._client

    def watch_changes(self, processor: "IChangeProcessor", pipeline: "_Pipeline"):
        with self.database.watch(pipeline, full_document="updateLookup") as stream:
            for raw_change in stream:
                change = Change(**raw_change)
                processor.process(change)
