from abc import ABC, abstractmethod
from typing import Any
from logging import getLogger

from typesense.client import Client
from typesense import exceptions as e

from app.core.configs.typesense_config import ComponentCollections, schemas, config_dict
from app.schemas.base import BaseDbSchema
from app.repos.component_repo import repos, IComponentRepo


logger = getLogger("app")


client = Client(config_dict=config_dict)


class SearchSchema(BaseDbSchema):
    model: str


class ISearchCollectionRepository(ABC):
    @abstractmethod
    def drop_collection(self, collection: ComponentCollections) -> None: ...

    @abstractmethod
    def drop_all_collections(self) -> None: ...

    @abstractmethod
    def init_collection(self, collection: ComponentCollections) -> None: ...

    @abstractmethod
    def init_all_collections(self) -> None: ...

    @abstractmethod
    def list_collections(self) -> list[str]: ...


class ISearchDocumentRepository(ABC):
    @abstractmethod
    def list_documents(self, collection: ComponentCollections) -> Any: ...


class TypesenseRepository(ISearchCollectionRepository, ISearchDocumentRepository):
    def __init__(self, client: Client) -> None:
        self._client = client

    # ---- Collections ----
    def drop_collection(self, collection: ComponentCollections) -> None:
        try:
            self._client.collections[collection].delete()
            logger.info("Deleted %s collection", collection)
        except e.ObjectNotFound:
            logger.warning(
                "Tried to delete %s collection, but collection doesn't exist",
                collection,
            )

    def drop_all_collections(self) -> None:
        for collection in ComponentCollections:
            self.drop_collection(collection)

    def init_collection(self, collection: ComponentCollections) -> None:
        try:
            self._client.collections.create(schemas[collection])
            logger.info("%s collection was created", collection)
        except e.ObjectAlreadyExists:
            logger.info("%s collection already exists", collection)

    def init_all_collections(self) -> None:
        for collection in ComponentCollections:
            self.init_collection(collection)

    def list_collections(self) -> list[str]:
        collections_info = self._client.collections.retrieve()
        return [coll["name"] for coll in collections_info]

    # ---- Documents ----
    def list_documents(self, collection: ComponentCollections) -> Any:
        return self._client.collections[collection].documents.documents


def upload_data_to_collection(
    collection: ComponentCollections,
    documents: list[SearchSchema] | None = None,
):
    repo: IComponentRepo = repos[collection]

    documents = repo.collection._get_collection().find({})

    doc_inserted_count = 0
    for doc in documents:

        doc = SearchSchema.model_validate(doc).model_dump(mode="json")
        client.collections[collection].documents.upsert(doc)
        doc_inserted_count += 1

    return {"inserted": doc_inserted_count}
