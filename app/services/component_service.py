from abc import ABC, abstractmethod
from typing import Any, Type

from fastapi_filter.contrib.mongoengine import Filter

from app.repos.component_repo import (
    IComponentRepo,
    CpuRepo,
    GpuRepo,
    RamRepo,
    MbRepo,
    PsuRepo,
)
from app.repos.index_repo import SearchIndexRepo
from app.core.configs.typesense_config import ComponentType


COMPONENT_COUNT = 500


class IComponentService(ABC):
    @abstractmethod
    def find(
        self,
        filters: Filter,
        count: int = COMPONENT_COUNT,
        page: int = 1,
        per_page: int = 10,
    ) -> list[Any]: ...


class BaseComponentService(IComponentService):
    repo: Type[IComponentRepo]
    index_coll: ComponentType

    def __init__(self, index: SearchIndexRepo):
        self.index = index

    def find(
        self,
        filters,
        count=COMPONENT_COUNT,
        page=1,
        per_page: int = 10,
    ) -> list[Any]:

        if filters.model:
            search_result = self.index.search(
                coll=self.index_coll,
                query=filters.model,
                page=page,
                per_page=per_page,
            )
            ids = [doc.id for doc in search_result.hits]

            filters.model = None
            filters.id__in = ids

            search_result.found
            search_result.request_params.per_page

        return self.repo().find(filters, limit=count)


class CpuService(BaseComponentService):
    repo = CpuRepo
    index_coll = ComponentType.CPU


class GpuService(BaseComponentService):
    repo = GpuRepo
    index_coll = ComponentType.GPU


class RamService(BaseComponentService):
    repo = RamRepo
    index_coll = ComponentType.RAM


class MotherboardService(BaseComponentService):
    repo = MbRepo
    index_coll = ComponentType.MOTHERBOARD


class PsuService(BaseComponentService):
    repo = PsuRepo
    index_coll = ComponentType.PSU
