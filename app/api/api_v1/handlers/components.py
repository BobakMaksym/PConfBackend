from typing import Annotated
from fastapi import APIRouter, Query

from app.core import utils
from app.filters import (
    CpuFilters,
    GpuFilters,
    MotherboardFilters,
    PsuFilters,
    RamFilters,
)
from app.services.component_service import (
    CpuService,
    GpuService,
    RamService,
    PsuService,
    MotherboardService,
)

component_router = APIRouter()


@component_router.get("/find/cpu", summary="Find CPUs")
async def find_cpu(
    # filters: CpuFilters = Query(...),
    filters: Annotated[CpuFilters, Query(...)],
    # count: int = Query(12, description="Number of CPUs to return"),
):
    result = CpuService.find(filters)
    return utils.json_encoder([r.model_dump(by_alias=True) for r in result])


@component_router.get("/find/gpu", summary="Find GPUs")
async def find_gpu(
    filters: GpuFilters = Query(...),
    # count: int = Query(12, description="Number of GPUs to return"),
):
    result = GpuService.find(filters)
    return utils.json_encoder([r.model_dump(by_alias=True) for r in result])


@component_router.get("/find/ram", summary="Find RAM modules")
async def find_ram(
    filters: RamFilters = Query(...),
    # count: int = Query(12, description="Number of RAM modules to return"),
):
    result = RamService.find(filters)
    return utils.json_encoder([r.model_dump(by_alias=True) for r in result])


@component_router.get("/find/motherboard", summary="Find motherboards")
async def find_motherboard(
    filters: MotherboardFilters = Query(...),
    # count: int = Query(12, description="Number of motherboards to return"),
):
    result = MotherboardService.find(filters)
    return utils.json_encoder([r.model_dump(by_alias=True) for r in result])


@component_router.get("/find/psu", summary="Find power supplies")
async def find_psu(
    filters: PsuFilters = Query(...),
    # count: int = Query(12, description="Number of PSUs to return"),
):
    result = PsuService.find(filters)
    return utils.json_encoder([r.model_dump(by_alias=True) for r in result])
