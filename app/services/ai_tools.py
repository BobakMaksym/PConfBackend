from copy import deepcopy
from functools import wraps
from typing import Any, Callable, cast
import logging

from agents import RunContextWrapper, function_tool

from app.core.configs.typesense_config import get_client
from app.filters.filters_ai import (
    CpuFilters,
    GpuFilters,
    RamFilters,
    MotherboardFilters,
    PsuFilters,
    SsdFilters,
)
from app.filters.component_filters import (
    CpuFilters as CpuDbFilters,
    GpuFilters as GpuDbFilters,
    RamFilters as RamDbFilters,
    MotherboardFilters as MotherboardDbFilters,
    PsuFilters as PsuDbFilters,
    SsdFilters as SsdDbFilters,
)
from app.schemas.pc_config_schema import (
    ComponentsSchema,
    PcConfigContext,
    PcConfigSchema,
)
from app.schemas.component_schema import (
    CpuSchema,
    GpuSchema,
    RamSchema,
    MotherboardSchema,
    PowerSupplySchema,
    SsdSchema,
)
from app.services.component_service import (
    CpuService,
    GpuService,
    RamService,
    MotherboardService,
    PsuService,
    SsdService,
)
from app.repos import config_repo
from app.core.paginator import Page
from app.repos.index_repo import (
    CpuIndexRepo,
    GpuIndexRepo,
    RamIndexRepo,
    PsuIndexRepo,
    MotherboardIndexRepo,
    SsdIndexRepo,
)

COMPONENT_COUNT = 2

logger = logging.getLogger("app")


def function_tool_find_decorator(func: Callable):
    """Decorator: normalizes filters and applies function_tool."""

    @function_tool
    @wraps(func)
    def wrapper(filters, page: int = 1):

        # logger.debug(type(filters))

        # filters = normalize_filters(filters)
        logger.debug("%s filters: %s", func.__name__, filters)

        components: list[Any] = func(filters, page)

        comps_copy = deepcopy(components)
        comps_copy.data = None

        logger.debug("find components: %s", comps_copy)

        return components

    return wrapper


# function_tool_find_decorator = function_tool


def function_tool_find_decorator(func: Callable):
    @function_tool
    @wraps(func)
    def wrapper(filters: CpuFilters, page: int = 1):
        logger.debug("%s filters: %s", func.__name__, filters)
        components: list[Any] = func(filters, page)
        return components

    return wrapper


client = get_client()
CpuIndexRepo(client=client)
GpuIndexRepo(client=client)
RamIndexRepo(client=client)
PsuIndexRepo(client=client)
MotherboardIndexRepo(client=client)


@function_tool_find_decorator
def find_cpu(filters: CpuFilters, page: int = 1) -> list[CpuSchema]:
    """finds CPU's in DB"""

    filters = CpuDbFilters(**filters.model_dump(mode="json"))

    return CpuService(CpuIndexRepo(client=client)).find(filters=filters, page=page).data


@function_tool_find_decorator
def find_gpu(filters: GpuFilters, page: int = 1) -> list[GpuSchema]:
    """finds GPU's in DB"""

    filters = GpuDbFilters(**filters.model_dump(mode="json"))

    return GpuService(GpuIndexRepo(client=client)).find(filters=filters, page=page).data


@function_tool_find_decorator
def find_ram(filters: RamFilters, page: int = 1) -> list[RamSchema,]:
    """finds RAM modules in DB"""

    filters = RamDbFilters(**filters.model_dump(mode="json"))

    return RamService(RamIndexRepo(client=client)).find(filters=filters, page=page).data


@function_tool_find_decorator
def find_motherboard(
    filters: MotherboardFilters, page: int = 1
) -> list[MotherboardSchema]:
    """finds motherboards in DB"""

    filters = MotherboardDbFilters(**filters.model_dump(mode="json"))

    return (
        MotherboardService(MotherboardIndexRepo(client=client))
        .find(filters=filters, page=page)
        .data
    )


@function_tool_find_decorator
def find_psu(filters: PsuFilters, page: int = 1) -> list[PowerSupplySchema]:
    """finds power supplies in DB"""

    filters = PsuDbFilters(**filters.model_dump(mode="json"))

    return PsuService(PsuIndexRepo(client=client)).find(filters=filters, page=page).data


@function_tool_find_decorator
def find_ssd(filters: SsdFilters, page: int = 1) -> list[SsdSchema]:
    """finds SSD's in DB"""

    filters = SsdDbFilters(**filters.model_dump(mode="json"))

    return SsdService(SsdIndexRepo(client=client)).find(filters=filters, page=page).data



@function_tool
def add_component(
    wrapper: RunContextWrapper[PcConfigContext],
    components: ComponentsSchema,
    # ):
) -> PcConfigSchema:
    """Adds a components to the PC config"""
    # logger.debug("\ncall add_component function\n")
    try:
        build_id = wrapper.context.id

        comp_types = components.model_dump(exclude_none=True).keys()
        for comp_t in comp_types:
            comp_id = getattr(components, comp_t)
            config_repo.add_component(build_id, comp_t, comp_id)

        build = cast(PcConfigSchema, config_repo.get_full_build(build_id))
        return build

    except Exception as e:
        logger.critical("\n\nerror: %s\n", e)
        raise


@function_tool
def get_configuration(wrapper: RunContextWrapper[PcConfigContext]):
    """Get the current state of the PC config"""
    id_ = wrapper.context.id
    build = config_repo.get_full_build(id_)

    return build
