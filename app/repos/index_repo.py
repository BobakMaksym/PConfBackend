from logging import getLogger

from typesense.client import Client
from typesense.collection import Collection
from typesense import exceptions as e
from typesense.types.document import SearchParameters
from typesense.types.collection import CollectionCreateSchema

from app.core.configs.typesense_config import ComponentType
from app.schemas.index_schema import IndexSchema
from app.schemas.index_search_res_schema import SearchResultSchema


logger = getLogger("app")


class SearchIndexRepo:
    """
    Repository for working with the Typesense
    """

    def __init__(self, client: "Client"):
        self._client = client

    @property
    def client(self):
        return self._client

    def _search(
        self,
        coll: ComponentType,
        search_params: SearchParameters,
    ):
        search_res = self.client.collections[coll].documents.search(
            search_parameters=search_params
        )
        return search_res

    def search(self, coll: ComponentType, query: str, page: int = 1):
        raw_search_result = self._search(
            coll=coll,
            search_params={
                "q": query,
                "query_by": "model",
                "page": page,
                "per_page": 10,
            },
        )
        return raw_search_result

    def ai_search(self, coll: ComponentType, query: str, page: int = 1):
        raw_search_result = self.search(coll, query, page)
        return SearchResultSchema(**raw_search_result)

    def get_coll(self, coll: ComponentType) -> Collection | None:
        """
        returns a collection object
        """
        try:
            # check if the collection exists
            self.client.collections[coll].retrieve()
            # return the collection
            return self.client.collections[coll]
        except e.ObjectNotFound:
            msg = "Tried to get collection %s, but collection doesn't exist"
            logger.warning(msg, coll)

    def create(self, schema: CollectionCreateSchema):
        """
        creates a specific collection according to the scheme
        """
        coll = schema["name"]
        try:
            self._client.collections.create(schema=schema)
            logger.info("%s collection was created", coll)
        except e.ObjectAlreadyExists:
            logger.info("%s collection already exists", coll)

    def drop(self, coll: ComponentType):
        """
        deletes a specific collection and data
        """
        try:
            self._client.collections[coll].delete()
            logger.info("Deleted %s collection", coll)
        except e.ObjectNotFound:
            msg = "Tried to delete %s collection, but collection doesn't exist"
            logger.warning(msg, coll)

    def list_coll(self) -> list[str]:
        """
        lists the collections created in the index
        """
        coll_info = self.client.collections.retrieve()
        return [coll["name"] for coll in coll_info]

    def add_all_docs_to_coll(
        self,
        coll: ComponentType,
        docs: list[IndexSchema],
    ) -> None:
        coll = self.get_coll(coll=coll)
        if not coll:
            raise e.ObjectNotFound(f"{coll} collection doesn't exist")

        index_docs = [doc.model_dump(mode="json") for doc in docs]

        coll.documents.import_(documents=index_docs)
