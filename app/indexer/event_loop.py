import logging

from mongoengine import connect
from typesense.client import Client

from app.core.config import settings

connect(db=settings.DATABASE, host=settings.MONGO_CONNECTION_STRING)

from app.db import db
from app.core.configs.typesense_config import config_dict
from app.schemas.change_stream_schema import ChangeStreamSchema
from app.schemas.base import BaseDbSchema


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("start")


ts_client = Client(config_dict=config_dict)


class DocumentSchema(BaseDbSchema):
    model: str


pipeline = [
    {
        "$match": {
            "operationType": {"$in": ["insert", "update", "delete"]},
            "ns.coll": {"$in": ["cpu", "gpu", "motherboard", "psu", "ram"]},
        }
    }
]


def run():
    with db.watch(pipeline, full_document="updateLookup") as stream:

        for change in stream:

            change = ChangeStreamSchema(**change)

            if change.operation_type == "delete":

                id = str(change.id)
                coll = change.ns.coll

                ts_client.collections[coll].documents[id].delete()

                logger.info("delete %s in %s", str(id), coll)

            elif change.operation_type == "update":

                if not change.update_description:
                    continue

                id = change.id
                coll = change.ns.coll

                document = DocumentSchema(
                    id=id,
                    model=change.update_description["updatedFields"]["model"],
                ).model_dump(mode="json")
                ts_client.collections[coll].documents.upsert(document)  # type: ignore

                logger.info("upsert %s in %s", str(id), coll)

            elif change.operation_type == "insert":

                if not change.full_document:
                    continue

                id = change.id
                coll = change.ns.coll

                document = DocumentSchema(
                    id=id,
                    model=change.full_document["model"],
                ).model_dump(mode="json")
                ts_client.collections[coll].documents.upsert(document)  # type: ignore

                logger.info("insert* or update %s in %s", str(id), coll)
