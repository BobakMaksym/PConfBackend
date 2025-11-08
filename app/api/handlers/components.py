from typing import Type
import logging

from fastapi import APIRouter, Query
from fastapi_filter import FilterDepends
from fastapi_filter.contrib.mongoengine import Filter

from app.filters.component_filters import (
    CpuFilters,
    GpuFilters,
    MotherboardFilters,
    PsuFilters,
    RamFilters,
    SsdFilters,
)
from app.services.component_service import (
    IComponentService,
    CpuService,
    GpuService,
    RamService,
    PsuService,
    MotherboardService,
    SsdService,
)
from app.core.configs.typesense_config import get_client
from app.repos.index_repo import (
    CpuIndexRepo,
    GpuIndexRepo,
    MotherboardIndexRepo,
    PsuIndexRepo,
    RamIndexRepo,
    SsdIndexRepo,
)

component_router = APIRouter()

logger = logging.getLogger("app")

index_client = get_client()
cpu_service = CpuService(CpuIndexRepo(client=index_client))
gpu_service = GpuService(GpuIndexRepo(client=index_client))
ram_service = RamService(RamIndexRepo(client=index_client))
motherboard_service = MotherboardService(MotherboardIndexRepo(client=index_client))
psu_service = PsuService(PsuIndexRepo(client=index_client))
ssd_service = SsdService(SsdIndexRepo(client=index_client))


def make_find_endpoint(
    path: str,
    endpoint_name: str,
    filter_model: Type[Filter],
    service_class: IComponentService,
    summary: str | None = None,
):
    async def endpoint(
        filters: Filter = FilterDepends(filter_model),
        page: int = Query(default=1, gt=0),
        per_page: int = Query(default=10, gt=0, lt=100),
        sort_by: list[str] | None = Query(default=None, example=["id", "-cores"]),
    ):
        component_page = service_class.find(
            filters=filters,
            page=page,
            per_page=per_page,
            sort_by=sort_by,
        )
        return component_page.model_dump(mode="json")

    endpoint.__name__ = endpoint_name

    component_router.get(path, summary=summary)(endpoint)


make_find_endpoint("/cpu", "find_cpu", CpuFilters, cpu_service, "Find CPUs")
make_find_endpoint("/gpu", "find_gpu", GpuFilters, gpu_service, "Find GPUs")
make_find_endpoint("/ram", "find_ram", RamFilters, ram_service, "Find RAM modules")
make_find_endpoint("/ssd", "find_ssd", SsdFilters, ssd_service, "Find SSDs")
make_find_endpoint(
    "/motherboard",
    "find_motherboard",
    MotherboardFilters,
    motherboard_service,
    "Find motherboards",
)
make_find_endpoint("/psu", "find_psu", PsuFilters, psu_service, "Find PSUs")
