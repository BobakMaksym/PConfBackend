from abc import ABC, abstractmethod
from typing import Any

from app.repos.component_repo import (
    IComponentRepo,
    CpuRepo,
    GpuRepo,
    RamRepo,
    MbRepo,
    PsuRepo,
)


COMPONENT_COUNT = 500


class IComponentService(ABC):
    @classmethod
    @abstractmethod
    def find(
        cls,
        filters: dict,
        count: int = COMPONENT_COUNT,
    ) -> list[Any]: ...


class BaseComponentService(IComponentService):
    repo: IComponentRepo

    @classmethod
    def find(cls, filters, count=COMPONENT_COUNT) -> list[Any]:
        # filters = normalize_filters(filters)
        return cls.repo().find(filters, limit=count)


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
