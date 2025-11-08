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
    SsdRepo,
)
from app.repos.index_repo import IComponentIndexRepo


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

    def __init__(self, index: IComponentIndexRepo):
        self.index = index

    def find(
        self,
        filters,
        page=1,
        per_page: int = 10,
        sort_by: Iterable[str] | None = None,
    ) -> Page:
        try:
            model = filters.model  # type: ignore

            if model:
                logger.info("the index paginator worked")

                paginator = IndexPaginator(self.index)
                requested_page = paginator.paginate(
                    filters=filters, page=page, per_page=per_page, sort_by=sort_by
                )

                logger.critical("\n\npage:\n%s", requested_page)

                return requested_page

            logger.info("the database paginator worked")

            paginator = Paginator(repo=self.repo())
            requested_page = paginator.paginate(
                filters=filters, page=page, per_page=per_page, sort_by=sort_by
            )

            logger.critical("\n\npage:\n%s", requested_page)

            return requested_page

        except Exception as e:
            logger.error("error: %s", e)
            raise


class CpuService(BaseComponentService):
    repo = CpuRepo


class GpuService(BaseComponentService):
    repo = GpuRepo


class RamService(BaseComponentService):
    repo = RamRepo


class MotherboardService(BaseComponentService):
    repo = MbRepo


class PsuService(BaseComponentService):
    repo = PsuRepo


class SsdService(BaseComponentService):
    repo = SsdRepo
