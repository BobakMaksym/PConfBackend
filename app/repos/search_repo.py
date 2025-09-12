from abc import ABC, abstractmethod
from typing import Any
from logging import getLogger

from typesense.client import Client
from typesense.collection import Collection
from typesense import exceptions as e
from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.core.configs.typesense_config import ComponentCollections, schemas, config_dict
from app.schemas.base import BaseDbSchema


logger = getLogger("app")


client = Client(config_dict=config_dict)


class SearchSchema(BaseDbSchema):
    model: str


class IIndexRepo(ABC):
    collection: ComponentCollections

    @abstractmethod
    def __init__(self, client: Any): ...

    @property
    @abstractmethod
    def coll(self) -> Collection: ...

    # Collections

    @abstractmethod
    def init_collection(self) -> None: ...

    @abstractmethod
    def drop_collection(self) -> None: ...

    # Documents

    @abstractmethod
    def upsert_doc(self, doc: SearchSchema): ...

    @abstractmethod
    def delete_doc(self, id: MongoObjectId): ...

    @abstractmethod
    def list_documents(self) -> Any: ...


class ICollectionIndexRepo(ABC):
    @abstractmethod
    def __init__(self, client):
        self._client = client

    # @abstractmethod
    # def add_collection(self, coll: ComponentCollections) -> None: ...

    # @abstractmethod
    # def drop_all_collections(self) -> None: ...

    # @abstractmethod
    # def init_all_collections(self) -> None: ...

    @abstractmethod
    def list_collections(self) -> list[str]: ...


class BaseTypesenseRepo(IIndexRepo):
    collection: ComponentCollections

    def __init__(self, client: Client) -> None:
        self._client = client

    @property
    def coll(self) -> Collection:
        return self._client.collections[self.collection]

    # ---- Collections ----

    def init_collection(self) -> None:
        try:
            self._client.collections.create(schemas[self.collection])
            logger.info("%s collection was created", self.collection)
        except e.ObjectAlreadyExists:
            logger.info("%s collection already exists", self.collection)

    def drop_collection(self) -> None:
        try:
            self._client.collections[self.collection].delete()
            logger.info("Deleted %s collection", self.collection)
        except e.ObjectNotFound:
            logger.warning(
                "Tried to delete %s collection, but collection doesn't exist",
                self.collection,
            )

    # ---- Documents ----

    def upsert_doc(self, doc: SearchSchema):
        self.coll.documents.upsert(doc.model_dump(mode="json"))

    def delete_doc(self, id: MongoObjectId):
        self.coll.documents[str(id)].delete()

    def list_documents(self) -> Any:
        return self.coll.documents.documents


class TypesenseCollIndexRepo(ICollectionIndexRepo):
    def __init__(self, client: Client):
        self._client = client
        self._cols: set[Collection] = set()

    # def add_collection(self, coll: ComponentCollections):
    #     ts_coll = self._client.collections[coll]
    #     self._cols.add(ts_coll)

    # def drop_all_collections(self) -> None:
    #     for coll in self._cols:
    #         self.drop_collection(collection)

    # def init_all_collections(self) -> None:
    #     for coll in self._cols:
    #         self.init_collection(collection)

    def list_collections(self) -> list[str]:
        collections_info = self._client.collections.retrieve()
        return [coll["name"] for coll in collections_info]


class CpuIndexRepo(BaseTypesenseRepo):
    collection = ComponentCollections.CPU


class GpuIndexRepo(BaseTypesenseRepo):
    collection = ComponentCollections.GPU


class RamIndexRepo(BaseTypesenseRepo):
    collection = ComponentCollections.RAM


class PsuIndexRepo(BaseTypesenseRepo):
    collection = ComponentCollections.PSU


class MotherboardIndexRepo(BaseTypesenseRepo):
    collection = ComponentCollections.MOTHERBOARD
