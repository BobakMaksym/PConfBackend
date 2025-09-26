from abc import ABC, abstractmethod
from typing import Type, Iterable

from fastapi_filter.contrib.mongoengine import Filter

from app.core.paginator import Paginator, Page
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


class IComponentService(ABC):
    @abstractmethod
    def find(
        self,
        filters: Filter,
        page: int = 1,
        per_page: int = 10,
        sort_by: Iterable[str] | None = None,
    ) -> Page: ...


class BaseComponentService(IComponentService):
    repo: Type[IComponentRepo]
    index_coll: ComponentType

    def __init__(self, index: SearchIndexRepo):
        self.index = index

    def find(
        self,
        filters,
        page=1,
        per_page: int = 10,
        sort_by: Iterable[str] | None = None,
    ) -> Page:

        model = filters.model  # type: ignore
        filters.model = None  # type: ignore

        # retrieve the count of documents from DB
        component_count = self.repo().count(filters=filters)

        # searching for models in the index and adding the found IDs to filters
        if model:
            # get all documents on one page
            search_result = self.index.search(
                coll=self.index_coll,
                query=model,
                page=1,
                per_page=component_count,
            )
            ids = [doc.id for doc in search_result.hits]

            filters.id__in = ids

        paginator = Paginator(repo=self.repo())
        requested_page = paginator.paginate(
            filters=filters, page=page, per_page=per_page, sort_by=sort_by
        )

        return requested_page


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
