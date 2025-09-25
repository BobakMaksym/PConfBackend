from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Type, Iterable

from fastapi_filter.contrib.mongoengine import Filter
from pydantic import BaseModel
from mongoengine import Document


@dataclass
class Page:
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
        document: Type[Document],
        filter: Type[Filter],
        schema: Type[BaseModel] | None = None,
    ): ...

    @abstractmethod
    def paginate(
        self,
        page: int,
        per_page: int = 10,
        filters: Filter | None = None,
        sort_by: Iterable[str] | None = None,
    ) -> Page: ...


class Paginator(IPaginator):
    def __init__(
        self,
        document: Type[Document],
        filter: Type[Filter],
        schema: Type[BaseModel] | None = None,
    ):
        self.document = document
        self.schema = schema
        self.filter = filter

    def paginate(
        self,
        page: int,
        per_page: int = 10,
        filters: Filter | None = None,
        sort_by: Iterable[str] | None = None,
    ):
        offset = (page - 1) * per_page

        # building a query

        cursor = self.document.objects().skip(offset).limit(per_page)  # type: ignore
        if sort_by:
            cursor = cursor.order_by(*sort_by)

        if filters:
            cursor = filters.filter(query=cursor)
            total_items = filters.filter(query=self.document.objects()).count()  # type: ignore
        else:
            total_items = self.document.objects.count()  # type: ignore

        total_pages = (total_items + per_page - 1) // per_page

        # data serialization

        if self.schema:
            data = [self.schema.model_validate(doc) for doc in cursor]
        else:
            data = list(cursor)

        has_next = True if page < total_pages else False
        has_prev = True if page > 1 else False

        return Page(
            curr_page=page,
            per_page=per_page,
            total_pages=total_pages,
            total_items=total_items,
            has_next=has_next,
            has_prev=has_prev,
            data=data,
        )
