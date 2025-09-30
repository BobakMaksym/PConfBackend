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
)
from app.services.component_service import (
    IComponentService,
    CpuService,
    GpuService,
    RamService,
    PsuService,
    MotherboardService,
)
from app.core.configs.typesense_config import ComponentType, get_client
from app.repos.index_repo import SearchIndexRepo

component_router = APIRouter()

logger = logging.getLogger("app")

index = SearchIndexRepo(client=get_client())


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


make_find_endpoint("/cpu", "find_cpu", CpuFilters, CpuService(index), "Find CPUs")
make_find_endpoint("/gpu", "find_gpu", GpuFilters, GpuService(index), "Find GPUs")
make_find_endpoint(
    "/ram", "find_ram", RamFilters, RamService(index), "Find RAM modules"
)
make_find_endpoint(
    "/motherboard",
    "find_motherboard",
    MotherboardFilters,
    MotherboardService(index),
    "Find motherboards",
)
make_find_endpoint("/psu", "find_psu", PsuFilters, PsuService(index), "Find PSUs")


@component_router.get("/search/{component_type}")
async def search_component(
    component_type: ComponentType,
    query: str,
    page: int = Query(default=1, gt=0),
    per_page: int = Query(default=1, gt=0),
):
    res = index.search(component_type, query, page, per_page)
    return res


# @component_router.get("/find/cpu", summary="Find CPUs")
# async def find_cpu(
#     filters: CpuFilter = FilterDepends(CpuFilter),
# ):
#     result = CpuService.find(filters)
#     return utils.json_encoder([r.model_dump(by_alias=True) for r in result])


# @component_router.get("/find/gpu", summary="Find GPUs")
# async def find_gpu(
#     filters: GpuFilters = Query(...),
#     # count: int = Query(12, description="Number of GPUs to return"),
# ):
#     result = GpuService.find(filters)
#     return utils.json_encoder([r.model_dump(by_alias=True) for r in result])


# @component_router.get("/find/ram", summary="Find RAM modules")
# async def find_ram(
#     filters: RamFilters = Query(...),
#     # count: int = Query(12, description="Number of RAM modules to return"),
# ):
#     result = RamService.find(filters)
#     return utils.json_encoder([r.model_dump(by_alias=True) for r in result])


# @component_router.get("/find/motherboard", summary="Find motherboards")
# async def find_motherboard(
#     filters: MotherboardFilters = Query(...),
#     # count: int = Query(12, description="Number of motherboards to return"),
# ):
#     result = MotherboardService.find(filters)
#     return utils.json_encoder([r.model_dump(by_alias=True) for r in result])


# @component_router.get("/find/psu", summary="Find power supplies")
# async def find_psu(
#     filters: PsuFilters = Query(...),
#     # count: int = Query(12, description="Number of PSUs to return"),
# ):
#     result = PsuService.find(filters)
#     return utils.json_encoder([r.model_dump(by_alias=True) for r in result])
