from bson import ObjectId

from app.helpers import COLLECTIONS
from app.models import Build as BuildState
from app.repo import BuildRepo, ComponentRepo



class BuildService:
    """
    BuildService — `Facade` for UI and AI agent
    """

    def __init__(self, db):
        self.cpu_repo = ComponentRepo(db, "cpu")
        self.mb_repo = ComponentRepo(db, "motherboard")
        self.ram_repo = ComponentRepo(db, "ram")
        self.psu_repo = ComponentRepo(db, "psu")

        self.build_repo = BuildRepo(db)

    # ---------- Пошук компонентів ----------
    def search_components(self, type_: COLLECTIONS, filters: dict, *, limit=20):
        repo: ComponentRepo = getattr(self, f"{type_}_repo")
        return repo.find(filters, limit=limit)

    # ---------- Операції зі збіркою ----------
    def add_component(
        self, build_id: ObjectId, type_: COLLECTIONS, component_id: ObjectId
    ):
        build = self.build_repo.load(build_id)
        if not build:
            raise ValueError("Unknown build")

        build.state[type_] = component_id
        self.build_repo.save_state(build_id, build.state)

    def remove_component(self, build_id: ObjectId, type_: COLLECTIONS):
        build = self.build_repo.load(build_id)
        if not build:
            raise ValueError("Unknown build")

        build.state.pop(type_, None)
        self.build_repo.save_state(build_id, build.state)

    def get_build(self, build_id: ObjectId) -> BuildState:
        b = self.build_repo.load(build_id)
        if not b:
            raise ValueError("Unknown build")
        return b
