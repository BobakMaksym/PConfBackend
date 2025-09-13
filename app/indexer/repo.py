from abc import ABC, abstractmethod

from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.repos.search_repo import SearchSchema


class IIndexRepo(ABC):
    @abstractmethod
    def delete(self, collection: str, id: MongoObjectId) -> None: ...

    @abstractmethod
    def upsert(self, collection: str, doc: SearchSchema) -> None: ...


class TypesenseIndexRepo(IIndexRepo):
    def __init__(self, client):
        self.client = client

    def delete(self, collection: str, id: MongoObjectId) -> None:
        self.client.collections[collection].documents[str(id)].delete()

    def upsert(self, collection: str, doc: SearchSchema) -> None:
        self.client.collections[collection].documents.upsert(
            doc.model_dump(mode="json")
        )
