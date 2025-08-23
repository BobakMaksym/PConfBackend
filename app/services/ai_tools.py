from functools import wraps
from typing import Any, Callable
import logging

from agents import RunContextWrapper, function_tool

from app.db import db
from app.filters import (
    CpuFilters,
    GpuFilters,
    RamFilters,
    MotherboardFilters,
    PsuFilters,
)
from app.helpers import normalize_filters
from app.schemas.pc_config_schema import Components, PcConfig, PcConfigContext
from app.schemas.component_schema import (
    Cpu,
    Gpu,
    Ram,
    Motherboard,
    PowerSupply,
)
from app.repos.component_repo import CpuRepo, GpuRepo, RamRepo, MbRepo, PsuRepo
from app.repos import config_repo


COMPONENT_COUNT = 2

logger = logging.getLogger("app")


def function_tool_and_filter_normalizer(func: Callable):
    """Decorator: normalizes filters and applies function_tool."""

    @function_tool
    @wraps(func)
    def wrapper(filters, count):

        filters = normalize_filters(filters)
        logger.debug("%s filters: %s", func.__name__, filters)

        components: list[Any] = func(filters, count)

        return components

    return wrapper


@function_tool_and_filter_normalizer
def find_cpu(filters: CpuFilters, count: int = COMPONENT_COUNT) -> list[Cpu]:
    """finds CPU's in DB"""
    return CpuRepo(db).find(filters, limit=count)


@function_tool_and_filter_normalizer
def find_gpu(filters: GpuFilters, count: int = COMPONENT_COUNT) -> list[Gpu]:
    """finds GPU's in DB"""
    return GpuRepo(db).find(filters, limit=count)


@function_tool_and_filter_normalizer
def find_ram(filters: RamFilters, count: int = COMPONENT_COUNT) -> list[Ram]:
    """finds RAM modules in DB"""
    return RamRepo(db).find(filters, limit=count)


@function_tool_and_filter_normalizer
def find_motherboard(
    filters: MotherboardFilters, count: int = COMPONENT_COUNT
) -> list[Motherboard]:
    """finds motherboards in DB"""
    return MbRepo(db).find(filters, limit=count)


@function_tool_and_filter_normalizer
def find_psu(filters: PsuFilters, count: int = COMPONENT_COUNT) -> list[PowerSupply]:
    """finds power supplies in DB"""
    return PsuRepo(db).find(filters, limit=count)


@function_tool
def add_component(
    wrapper: RunContextWrapper[PcConfigContext],
    components: Components,
):
    """Adds a components to the PC config"""
    build_id = wrapper.context._id

    comp_types = components.model_dump(exclude_none=True).keys()
    for comp_t in comp_types:
        comp_id = getattr(components, comp_t)
        config_repo.add_component(build_id, comp_t, comp_id)

    build = config_repo.get_full_build(build_id)

    return build


@function_tool
def get_configuration(wrapper: RunContextWrapper[PcConfigContext]):
    """Get the current state of the PC config"""
    id_ = wrapper.context._id
    build = config_repo.get_full_build(id_)

    return build
