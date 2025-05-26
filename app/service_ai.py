from agents import function_tool
from pymongo import MongoClient

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


component_repos = {
    "cpu": CpuRepo(db),
    "gpu": GpuRepo(db),
    # "motherboard": ComponentRepo(db, "motherboard"),
    # "ram": ComponentRepo(db, "ram"),
    # "psu": ComponentRepo(db, "psu"),
}
build_repo = BuildRepo(db)


# ---------- Пошук компонентів ----------
@function_tool
def search_components(
    component_type: COLLECTIONS,
    manufacturer: str | None = None,
    cores: int | None = None,
    count: int = 5,
) -> list[Cpu]:  # List[Dict[str, Any]]:
    """finds components in the database"""

    filters = {"manufacturer": manufacturer, "cores": cores}
    filters = normalize_filters(filters)
    print(component_type, count, filters, flush=True)

    repo: BaseComponentRepo = component_repos.get(component_type)

    components = repo.find(filters, limit=count)

    return components


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
