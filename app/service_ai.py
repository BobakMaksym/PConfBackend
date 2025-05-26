# from bson import int
from typing import Dict, Any, List
import subprocess

from agents import function_tool
from pymongo import MongoClient

from app.helpers import COLLECTIONS, normalize_filters
from app.models import Build as BuildState, Cpu, Gpu
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
def add_component(build_id: int, type_: str, component_id: int):
    build = build_repo.load(build_id)
    if not build:
        raise ValueError("Unknown build")

    build.state[type_] = component_id
    build_repo.save_state(build_id, build.state)


@function_tool
def remove_component(build_id: int, type_: str):
    build = build_repo.load(build_id)
    if not build:
        raise ValueError("Unknown build")

    build.state.pop(type_, None)
    build_repo.save_state(build_id, build.state)


@function_tool
def get_build(build_id: int) -> BuildState:
    b = build_repo.load(build_id)
    if not b:
        raise ValueError("Unknown build")
    return b
