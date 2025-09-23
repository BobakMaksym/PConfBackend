from typing import Type
import logging

from fastapi import APIRouter, Request
from fastapi_filter import FilterDepends
from pydantic import BaseModel

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
from app.core.configs.typesense_config import ComponentType

component_router = APIRouter()

logger = logging.getLogger("app")


def make_find_endpoint(
    path: str,
    endpoint_name: str,
    filter_model: Type[BaseModel],
    service_class: IComponentService,
    summary: str | None = None,
):
    async def endpoint(filters: filter_model = FilterDepends(filter_model)):
        components = service_class.find(filters)
        return [
            component.model_dump(mode="json", by_alias=True) for component in components
        ]

    endpoint.__name__ = endpoint_name

    component_router.get(path, summary=summary)(endpoint)


make_find_endpoint("/cpu", "find_cpu", CpuFilters, CpuService(), "Find CPUs")
make_find_endpoint("/gpu", "find_gpu", GpuFilters, GpuService(), "Find GPUs")
make_find_endpoint("/ram", "find_ram", RamFilters, RamService(), "Find RAM modules")
make_find_endpoint(
    "/motherboard",
    "find_motherboard",
    MotherboardFilters,
    MotherboardService(),
    "Find motherboards",
)
make_find_endpoint("/psu", "find_psu", PsuFilters, PsuService(), "Find PSUs")


@component_router.get("/search/{component_type}")
async def search_component(
    request: Request,
    component_type: ComponentType,
    query: str,
    page: int = 1,
):
    res = request.app.state.search_index.search(component_type, query, page)
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
