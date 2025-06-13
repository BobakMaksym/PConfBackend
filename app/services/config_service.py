from app.helpers import COLLECTIONS
from app.schemas.component_schema import Build
from app.schemas.pyobjectid import PyObjectId
from app.repo import (
    BuildRepo,
    BaseComponentRepo,
    CpuRepo,
    GpuRepo,
    MbRepo,
    RamRepo,
    PsuRepo,
)


class BuildService:

    def __init__(self, db):
        self.repos = {
            "cpu": CpuRepo(db),
            "gpu": GpuRepo(db),
            "motherboard": MbRepo(db),
            "ram": RamRepo(db),
            "psu": PsuRepo(db),
        }
        self.build_repo = BuildRepo(db)

    def search_components(self, type_: COLLECTIONS, filters: dict, *, limit=20):

        repo: BaseComponentRepo = getattr(self.repos, f"{type_}_repo")
        return repo.find(filters, limit=limit)

    def add_component(
        self, build_id: PyObjectId, type_: COLLECTIONS, component_id: PyObjectId
    ):
        build = self.build_repo.load(build_id)
        if not build:
            raise ValueError("Unknown build")

        build.state[type_] = component_id
        self.build_repo.save_state(build_id, build.state)

    def remove_component(self, build_id: PyObjectId, type_: COLLECTIONS):
        build = self.build_repo.load(build_id)
        if not build:
            raise ValueError("Unknown build")

        build.state.pop(type_, None)
        self.build_repo.save_state(build_id, build.state)

    def get_build(self, build_id: PyObjectId) -> Build:
        b = self.build_repo.load(build_id)
        if not b:
            raise ValueError("Unknown build")
        return b

    def get_configuration(self, id_: PyObjectId):
        """Get the current state of the PC config"""

        _build = self.build_repo.get_full_build(id_)

        build = Build(**_build)

        return build
