from logging import getLogger
from pprint import pprint

from fastapi_filter.contrib.mongoengine import Filter
from typesense.client import Client
from typesense.collection import Collection
from typesense import exceptions as e
from typesense.types.document import SearchParameters
from typesense.types.collection import CollectionCreateSchema

from app.core.configs.typesense_config import ComponentType
from app.schemas.index_schema import IndexSchema
from app.schemas.index_search_res_schema import SearchResultSchema


logger = getLogger("app")


OPERATORS = {
    "exact": ":=",
    "gte": ":>=",
    "lte": ":<=",
    "gt": ":>",
    "lt": ":<",
    "in": ":=[{values}]",
}


def build_filter_by(filters: dict) -> str:
    expressions = []
    for key, value in filters.items():
        if value is None:
            continue

        # split "field__op"
        if "__" in key:
            field, op = key.split("__", 1)
        else:
            field, op = key, "exact"
            print(field, op)

        if op == "in":
            values = ",".join(map(str, value))
            expr = f"{field}:=[{values}]"
        else:
            expr = f"{field}{OPERATORS[op]}{value}"

        expressions.append(expr)

    return " && ".join(expressions)


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

    def search(
        self,
        coll: ComponentType,
        query: str,
        filter_by: Filter | None = None,
        page: int = 1,
        per_page: int = 10,
    ) -> SearchResultSchema:
        search_params: SearchParameters = {
            "q": query,
            "query_by": "model",
            "page": page,
            "per_page": per_page,
        }
        if filter_by:
            raw_filters = filter_by.model_dump(mode="json")
            filters = build_filter_by(raw_filters)
            search_params.update(filter_by=filters)

        logger.error(search_params)

        raw_search_result = self._search(
            coll=coll,
            search_params=search_params,
        )
        return SearchResultSchema.model_validate(raw_search_result)

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
