from typing import Annotated
from fastapi import APIRouter, Body, Depends, Query, status, Path
from fastapi.responses import Response

from app.api.deps.user_deps import get_current_user
from app.core import utils
from app.db import db
from app.filters import (
    CpuFilters,
    GpuFilters,
    MotherboardFilters,
    PsuFilters,
    RamFilters,
)
from app.helpers import COLLECTIONS
from app.documents.user_model import User
from app.repo import BuildRepo
from app.services.component_service import ConfigService
from app.schemas.component_schema import Build
from app.schemas.user_schema import UserOut
from app.services.config_service import BuildService
from app.services.user_service import UserService
from app.schemas.pyobjectid import PyObjectId

component_router = APIRouter()

service = BuildService(db)


@component_router.get("/find/cpu", summary="Find CPUs")
async def find_cpu(
    # filters: CpuFilters = Query(...),
    filters: Annotated[CpuFilters, Query(...)],
    # count: int = Query(12, description="Number of CPUs to return"),
):
    result = ConfigService().find_cpu(filters)
    return utils.json_encoder([r.model_dump(by_alias=True) for r in result])


@component_router.get("/find/gpu", summary="Find GPUs")
async def find_gpu(
    filters: GpuFilters = Query(...),
    # count: int = Query(12, description="Number of GPUs to return"),
):
    result = ConfigService().find_gpu(filters)
    return utils.json_encoder([r.model_dump(by_alias=True) for r in result])


@component_router.get("/find/ram", summary="Find RAM modules")
async def find_ram(
    filters: RamFilters = Query(...),
    # count: int = Query(12, description="Number of RAM modules to return"),
):
    result = ConfigService().find_ram(filters)
    return utils.json_encoder([r.model_dump(by_alias=True) for r in result])


@component_router.get("/find/motherboard", summary="Find motherboards")
async def find_motherboard(
    filters: MotherboardFilters = Query(...),
    # count: int = Query(12, description="Number of motherboards to return"),
):
    result = ConfigService().find_motherboard(filters)
    return utils.json_encoder([r.model_dump(by_alias=True) for r in result])


@component_router.get("/find/psu", summary="Find power supplies")
async def find_psu(
    filters: PsuFilters = Query(...),
    # count: int = Query(12, description="Number of PSUs to return"),
):
    result = ConfigService().find_psu(filters)
    return utils.json_encoder([r.model_dump(by_alias=True) for r in result])
