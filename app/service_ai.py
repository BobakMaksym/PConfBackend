from agents import function_tool
from pymongo import MongoClient

from app.filters import CpuFilters, GpuFilters
from app.helpers import COLLECTIONS, normalize_filters
from app.models import Build as BuildState, Cpu, Gpu, PyObjectId
from app.repo import BuildRepo, BaseComponentRepo, CpuRepo, GpuRepo


DB_NAME = "components"
MONGO_CONFIG = {
    "host": "localhost",
    "port": 27017,
    "username": "root",
    "password": "root",
}

client = MongoClient(**MONGO_CONFIG)
db = client[DB_NAME]


COMPONENT_COUNT = 5


component_repos = {
    "cpu": CpuRepo(db),
    "gpu": GpuRepo(db),
    # "motherboard": ComponentRepo(db, "motherboard"),
    # "ram": ComponentRepo(db, "ram"),
    # "psu": ComponentRepo(db, "psu"),
}
build_repo = BuildRepo(db)


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


find_cpu_api = find_cpu
find_gpu_api = find_gpu

find_cpu = function_tool(find_cpu)
find_gpu = function_tool(find_gpu)


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
