from bson import ObjectId

from agents import function_tool
from pymongo import MongoClient

from app.helpers import COLLECTIONS
from app.models import Build as BuildState
from app.repo import BuildRepo, ComponentRepo


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
    "cpu": ComponentRepo(db, "cpu"),
    "motherboard": ComponentRepo(db, "motherboard"),
    "ram": ComponentRepo(db, "ram"),
    "psu": ComponentRepo(db, "psu"),
}
build_repo = BuildRepo(db)


# ---------- Пошук компонентів ----------
@function_tool
def search_components(type_, filters: dict, *, limit=20):
    """finds components in the database"""
    repo = component_repos.get(type_)
    return repo.find(filters, limit=limit)


# ---------- Операції зі збіркою ----------
@function_tool
def add_component(build_id: ObjectId, type_, component_id: ObjectId):
    build = build_repo.load(build_id)
    if not build:
        raise ValueError("Unknown build")

    build.state[type_] = component_id
    build_repo.save_state(build_id, build.state)


@function_tool
def remove_component(build_id: ObjectId, type_):
    build = build_repo.load(build_id)
    if not build:
        raise ValueError("Unknown build")

    build.state.pop(type_, None)
    build_repo.save_state(build_id, build.state)


@function_tool
def get_build(build_id: ObjectId) -> BuildState:
    b = build_repo.load(build_id)
    if not b:
        raise ValueError("Unknown build")
    return b
