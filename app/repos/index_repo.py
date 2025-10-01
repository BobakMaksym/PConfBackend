from abc import ABC, abstractmethod
from logging import getLogger
from typing import Type

from fastapi_filter.contrib.mongoengine import Filter
from pydantic import BaseModel
from typesense.client import Client
from typesense import exceptions as e
from typesense.types.document import SearchParameters
from typesense.types.collection import CollectionCreateSchema

from app.core.configs.typesense_config import (
    ComponentType,
    schema_cpu,
    schema_ram,
    schema_gpu,
    schema_motherboard,
    schema_psu,
)
from app.core.configs.typesense_component_schemas import (
    BaseIndexSchema,
    CpuIndexSchema,
    RamIndexSchema,
    GpuIndexSchema,
    MotherboardIndexSchema,
    PowerSupplyIndexSchema,
)
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


class IComponentIndexRepo(ABC):
    coll: ComponentType
    index_coll_schema: CollectionCreateSchema
    schema: Type[BaseModel]

    @abstractmethod
    def __init__(self, client: Client): ...

    @abstractmethod
    def search(
        self,
        query: str,
        filter_by: Filter | None = None,
        page: int = 1,
        per_page: int = 10,
    ) -> SearchResultSchema: ...

    @abstractmethod
    def create(self) -> None: ...

    @abstractmethod
    def drop(self) -> None: ...

    @abstractmethod
    def add_all_docs_to_coll(self, docs: list[BaseIndexSchema]) -> None: ...


class BaseComponentIndexRepo(IComponentIndexRepo):
    coll: ComponentType
    index_coll_schema: CollectionCreateSchema
    schema: Type[BaseModel]

    def __init__(self, client: Client):
        self._client = client

    @property
    def client(self):
        return self._client

    def _search(self, search_params: SearchParameters):
        search_res = self.client.collections[self.coll].documents.search(
            search_parameters=search_params
        )
        return search_res

    def search(
        self,
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

        raw_search_result = self._search(search_params=search_params)

        return SearchResultSchema.model_validate(raw_search_result)

    def create(self):
        """
        creates a specific collection according to the scheme
        """
        try:
            self._client.collections.create(schema=self.index_coll_schema)
            logger.info("%s collection was created", self.coll)
        except e.ObjectAlreadyExists:
            logger.info("%s collection already exists", self.coll)

    def drop(self):
        """
        deletes a specific collection and data
        """
        try:
            self.client.collections[self.coll].delete()
            logger.info("Deleted %s collection", self.coll)
        except e.ObjectNotFound:
            msg = "Tried to delete %s collection, but collection doesn't exist"
            logger.warning(msg, self.coll)

    def add_all_docs_to_coll(
        self,
        docs: list[BaseIndexSchema],
    ) -> None:
        try:
            # check if the collection exists
            self.client.collections[self.coll].retrieve()
        except e.ObjectNotFound:
            # msg = "Tried to get collection %s, but collection doesn't exist"
            # logger.warning(msg, self.coll)
            raise e.ObjectNotFound(f"{self.coll} collection doesn't exist")

        index_docs = []
        for doc in docs:
            index_doc = doc.model_dump(mode="json", exclude_none=True)
            index_docs.append(index_doc)

        res = self.client.collections[self.coll].documents.import_(documents=index_docs)

        for i in res:
            print(i)


class CpuIndexRepo(BaseComponentIndexRepo):
    coll = ComponentType.CPU
    index_coll_schema = schema_cpu
    schema = CpuIndexSchema


class GpuIndexRepo(BaseComponentIndexRepo):
    coll = ComponentType.GPU
    index_coll_schema = schema_gpu
    schema = GpuIndexSchema


class RamIndexRepo(BaseComponentIndexRepo):
    coll = ComponentType.RAM
    index_coll_schema = schema_ram
    schema = RamIndexSchema


class PsuIndexRepo(BaseComponentIndexRepo):
    coll = ComponentType.PSU
    index_coll_schema = schema_psu
    schema = PowerSupplyIndexSchema


class MotherboardIndexRepo(BaseComponentIndexRepo):
    coll = ComponentType.MOTHERBOARD
    index_coll_schema = schema_motherboard
    schema = MotherboardIndexSchema
