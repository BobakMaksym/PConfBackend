from agents import function_tool
import dotenv
from pymongo import MongoClient
import os

from app.filters import (
    CpuFilters,
    GpuFilters,
    RamFilters,
    MotherboardFilters,
    PsuFilters,
)
from app.helpers import COLLECTIONS, normalize_filters
from app.models import (
    Build as BuildState,
    Cpu,
    Gpu,
    Ram,
    Motherboard,
    PowerSupply,
    PyObjectId,
)
from app.repo import (
    BuildRepo,
    BaseComponentRepo,
    CpuRepo,
    GpuRepo,
    RamRepo,
    MbRepo,
    PsuRepo,
)

dotenv.load_dotenv()

# MONGO_CONFIG = {
#     "host": "localhost",
#     "port": 27017,
#     "username": "root",
#     "password": "root",
# }
# client = MongoClient(**MONGO_CONFIG)


MONGODB_SRV = os.environ.get("MONGODB_SRV")
DB_NAME = "components"

client = MongoClient(MONGODB_SRV)
db = client[DB_NAME]
build_repo = BuildRepo(db)

COMPONENT_COUNT = 5


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


# API aliases (original functions)
find_cpu_api = find_cpu
find_gpu_api = find_gpu
find_ram_api = find_ram
find_motherboard_api = find_motherboard
find_psu_api = find_psu

# Decorated with function_tool for OpenAI agents
find_cpu = function_tool(find_cpu)
find_gpu = function_tool(find_gpu)
find_ram = function_tool(find_ram)
find_motherboard = function_tool(find_motherboard)
find_psu = function_tool(find_psu)


# ---------- Операції зі збіркою ----------
@function_tool
def add_component(build_id: PyObjectId, type_: COLLECTIONS, component_id: PyObjectId):
    """adds a component to the build"""
    build = build_repo.load(build_id)
    if not build:
        raise ValueError("Unknown build")

    build.state[type_] = component_id
    build_repo.save_state(build_id, build.state)


@function_tool
def remove_component(build_id: PyObjectId, type_: COLLECTIONS):
    """removes a component from the assembly"""
    build = build_repo.load(build_id)
    if not build:
        raise ValueError("Unknown build")

    build.state.pop(type_, None)
    build_repo.save_state(build_id, build.state)


@function_tool
def get_build(build_id: PyObjectId) -> BuildState:
    """get the user's PC from the database"""
    build = build_repo.load(build_id)
    if not build:
        raise ValueError("Unknown build")
    return build
