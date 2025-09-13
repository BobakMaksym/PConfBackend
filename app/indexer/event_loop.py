import logging

from mongoengine import connect
from typesense.client import Client

from app.core.config import settings
from app.core.configs.typesense_config import config_dict
from app.db import db
from app.schemas.change_stream_schema import ChangeStreamSchema

from app.indexer.dispatcher import ChangeStreamProcessor
from app.indexer.handler import DeleteHandler, InsertHandler, UpdateHandler
from app.indexer.repo import TypesenseIndexRepo


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("start")


connect(db=settings.DATABASE, host=settings.MONGO_CONNECTION_STRING)

ts_client = Client(config_dict=config_dict)
index_repo = TypesenseIndexRepo(client=ts_client)


pipeline = [
    {
        "$match": {
            "operationType": {"$in": ["insert", "update", "delete"]},
            "ns.coll": {"$in": ["cpu", "gpu", "motherboard", "psu", "ram"]},
        }
    }
]


processor = ChangeStreamProcessor(
    handlers={
        "delete": DeleteHandler(index_repo),
        "update": UpdateHandler(index_repo),
        "insert": InsertHandler(index_repo),
    }
)


def run():
    with db.watch(pipeline, full_document="updateLookup") as stream:
        for raw_change in stream:
            change = ChangeStreamSchema(**raw_change)
            processor.process(change)
