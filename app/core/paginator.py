from abc import ABC, abstractmethod
from typing import Any, Type, Iterable, TYPE_CHECKING

from fastapi_filter.contrib.mongoengine import Filter
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.repos.component_repo import IComponentRepo


class Page(BaseModel):
    curr_page: int
    per_page: int
    total_pages: int
    total_items: int
    has_next: bool
    has_prev: bool
    data: Any


class IPaginator(ABC):
    @abstractmethod
    def __init__(
        self,
        repo: Type["IComponentRepo"],
    ): ...

    @abstractmethod
    def paginate(
        self,
        filters: Filter,
        page: int = 1,
        per_page: int = 10,
        sort_by: Iterable[str] | None = None,
    ) -> Page: ...


class Paginator(IPaginator):
    def __init__(self, repo: "IComponentRepo"):
        self.repo = repo

    def paginate(
        self,
        filters: Filter,
        page: int = 1,
        per_page: int = 10,
        sort_by: Iterable[str] | None = None,
    ):
        offset = (page - 1) * per_page

        components = self.repo.filter(
            filters=filters,
            offset=offset,
            limit=per_page,
            sort_by=sort_by,
        )
        total_items = self.repo.count(filters=filters)

        total_pages = (total_items + per_page - 1) // per_page

        has_next = True if page < total_pages else False
        has_prev = True if page > 1 else False

        return Page(
            curr_page=page,
            per_page=per_page,
            total_pages=total_pages,
            total_items=total_items,
            has_next=has_next,
            has_prev=has_prev,
            data=components,
        )
