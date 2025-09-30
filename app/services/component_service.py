from abc import ABC, abstractmethod
from typing import Type, Iterable
import logging

from fastapi_filter.contrib.mongoengine import Filter

from app.core.paginator import Paginator, Page, IndexPaginator
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


logger = logging.getLogger("app")


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

        if model:
            logger.info("спрацював пагінатор по індексу")

            paginator = IndexPaginator(self.index, coll=self.index_coll)
            requested_page = paginator.paginate(
                filters=filters, page=page, per_page=per_page, sort_by=sort_by
            )
            return requested_page

        logger.info("спрацював пагінатор по БД")

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
