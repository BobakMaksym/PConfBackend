from abc import ABC, abstractmethod
from typing import Any, ClassVar

from app.db import db
from app.helpers import normalize_filters
from app.repo import (
    CpuRepo,
    GpuRepo,
    RamRepo,
    MbRepo,
    PsuRepo,
)


COMPONENT_COUNT = 500

# ###################################


# cpu_repo = CpuRepo(db)
# gpu_repo = GpuRepo(db)
# ram_repo = RamRepo(db)
# mb_repo = MbRepo(db)
# psu_repo = PsuRepo(db)


class AbstractComponentService(ABC):
    @classmethod
    @abstractmethod
    def find(cls, filters: dict, count: int) -> list[Any]: ...


class BaseComponentService(AbstractComponentService):
    repo: ClassVar = None

    @classmethod
    def find(cls, filters, count=COMPONENT_COUNT) -> list[Any]:
        filters = normalize_filters(filters)
        return cls.repo(db).find(filters, limit=count)


class CpuService(BaseComponentService):
    repo = CpuRepo


class GpuService(BaseComponentService):
    repo = GpuRepo


class RamService(BaseComponentService):
    repo = RamRepo


class CpuService(BaseComponentService):
    repo = CpuRepo


class MotherboardService(BaseComponentService):
    repo = MbRepo


class PsuService(BaseComponentService):
    repo = PsuRepo
