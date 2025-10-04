from abc import ABC, abstractmethod
import logging

from typesense.client import Client
from typesense import exceptions as ts_exc
from pydantic_extra_types.mongo_object_id import MongoObjectId

from enums import Collection
from schemas import IndexDoc


logger = logging.getLogger(__name__)


class IIndex(ABC):
    @abstractmethod
    def __init__(self, client: Client): ...

    @abstractmethod
    def delete(self, collection: Collection, id: MongoObjectId) -> None: ...

    @abstractmethod
    def upsert(self, collection: Collection, doc: IndexDoc) -> None: ...


class Index(IIndex):
    def __init__(self, client: Client):
        self.client = client

    def delete(self, collection: Collection, id: MongoObjectId) -> None:
        try:
            self.client.collections[collection].documents[str(id)].delete()

            msg = "Deleted document %s from collection '%s' in Typesense"
            logger.info(msg, id, collection)
        except ts_exc.ObjectNotFound as exc:
            msg = "Document %s not found in collection '%s' (Typesense). Error: %s"
            logger.warning(msg, id, collection, exc)
        except Exception as exc:
            msg = "Failed to delete document %s from collection '%s'. Unexpected error: %s"
            logger.error(msg, id, collection, exc, exc_info=True)
            raise

    def upsert(self, collection: Collection, doc: IndexDoc) -> None:
        try:
            new_doc = doc.model_dump(mode="json", exclude_none=True)
            response = self.client.collections[collection].documents.upsert(new_doc)

            msg = "Upserted document %r into collection %r in Typesense: %s"
            logger.info(msg, doc.id, collection, response)
        except Exception as exc:
            msg = "Unexpected error while upserting document %s into collection '%s'. Error: %s"
            logger.error(msg, doc.id, collection, exc, exc_info=True)
            raise
