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
from app.schemas.build import BuildContext, Components
from app.schemas.component_schema import (
    Build,
    Cpu,
    Gpu,
    Ram,
    Motherboard,
    PowerSupply,
)
from app.repo import (
    BuildRepo,
    ChatRepo,
    CpuRepo,
    GpuRepo,
    RamRepo,
    MbRepo,
    PsuRepo,
)


COMPONENT_COUNT = 2


build_repo = BuildRepo(db)
chat_repo = ChatRepo(db)


def find_cpu(filters: CpuFilters, count: int = COMPONENT_COUNT) -> list[Cpu]:
    """finds CPU's in DB"""
    filters = normalize_filters(filters)
    print(filters)
    return CpuRepo(db).find(filters, limit=count)


def find_gpu(filters: GpuFilters, count: int = COMPONENT_COUNT) -> list[Gpu]:
    """finds GPU's in DB"""
    filters = normalize_filters(filters)
    print(filters)
    return GpuRepo(db).find(filters, limit=count)


# RAM
def find_ram(filters: RamFilters, count: int = COMPONENT_COUNT) -> list[Ram]:
    """finds RAM modules in DB"""
    filters = normalize_filters(filters)
    print(filters)
    return RamRepo(db).find(filters, limit=count)


# Motherboard
def find_motherboard(
    filters: MotherboardFilters, count: int = COMPONENT_COUNT
) -> list[Motherboard]:
    """finds motherboards in DB"""
    filters = normalize_filters(filters)
    print(filters)
    return MbRepo(db).find(filters, limit=count)


# PSU
def find_psu(filters: PsuFilters, count: int = COMPONENT_COUNT) -> list[PowerSupply]:
    """finds power supplies in DB"""
    filters = normalize_filters(filters)
    print(filters)
    return PsuRepo(db).find(filters, limit=count)


# Decorated with function_tool for OpenAI agents
find_cpu = function_tool(find_cpu)
find_gpu = function_tool(find_gpu)
find_ram = function_tool(find_ram)
find_motherboard = function_tool(find_motherboard)
find_psu = function_tool(find_psu)


# ---------- Операції зі збіркою ----------
@function_tool
def add_component(
    wrapper: RunContextWrapper[BuildContext],
    components: Components,
):
    """Adds a components to the PC config"""

    build_id = wrapper.context._id

    comp_types = components.model_dump(exclude_none=True).keys()
    for comp_t in comp_types:
        comp_id = getattr(components, comp_t)
        build_repo.add_component(build_id, comp_t, comp_id)

    build = build_repo.get_full_build(build_id)

    return Build(**build)


@function_tool
def get_configuration(wrapper: RunContextWrapper[BuildContext]):
    """Get the current state of the PC config"""
    id_ = wrapper.context._id
    _build = build_repo.get_full_build(id_)

    build = Build(**_build)

    return build
