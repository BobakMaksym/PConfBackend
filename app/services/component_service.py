from app.db import db
from app.filters import (
    CpuFilters,
    GpuFilters,
    RamFilters,
    MotherboardFilters,
    PsuFilters,
)
from app.helpers import COLLECTIONS, normalize_filters
from app.schemas.build import BuildContext, Components
from app.schemas.pyobjectid import PyObjectId
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


COMPONENT_COUNT = 10

# ###################################


# build_repo = BuildRepo(db)
# cpu_repo = CpuRepo(db)
# gpu_repo = GpuRepo(db)
# ram_repo = RamRepo(db)
# mb_repo = MbRepo(db)
# psu_repo = PsuRepo(db)


class ConfigService:

    @staticmethod
    def create_build(user_id: PyObjectId) -> PyObjectId:
        """create a new build in the db"""

        build_id = BuildRepo(db).create(user_id)
        return build_id

    @staticmethod
    def delete_build(build_id: PyObjectId):
        BuildRepo(db).delete(build_id=build_id)

    # ---------- Операції зі збіркою ----------
    @staticmethod
    def add_component(build_id: PyObjectId, component: COLLECTIONS, component_id):
        """Adds a components to the PC config"""

        BuildRepo(db).add_component(build_id, component, component_id)

        build = BuildRepo(db).get_full_build(build_id)

        return Build(**build)

    @staticmethod
    def get_configuration(build_id: PyObjectId):
        """Get the current state of the PC config"""

        _build = BuildRepo(db).get_full_build(build_id)

        build = Build(**_build)

        return build

    @staticmethod
    def remove_component(build_id: PyObjectId, type_: COLLECTIONS):
        """removes a component from the assembly"""
        build = BuildRepo(db).get_config(build_id)
        if not build:
            raise ValueError("Unknown build")

        BuildRepo(db).col.update_one({"_id": build_id}, {"$unset": {type_: 1}})

    # ---------- пошук та фільтрація компонентів ----------

    @staticmethod
    def find_cpu(filters: CpuFilters, count: int = COMPONENT_COUNT) -> list[Cpu]:
        """finds CPU's in DB"""
        filters = normalize_filters(filters)
        return CpuRepo(db).find(filters, limit=count)

    @staticmethod
    def find_gpu(filters: GpuFilters, count: int = COMPONENT_COUNT) -> list[Gpu]:
        """finds GPU's in DB"""
        filters = normalize_filters(filters)
        return GpuRepo(db).find(filters, limit=count)

    # RAM
    @staticmethod
    def find_ram(filters: RamFilters, count: int = COMPONENT_COUNT) -> list[Ram]:
        """finds RAM modules in DB"""
        filters = normalize_filters(filters)
        return RamRepo(db).find(filters, limit=count)

    # Motherboard
    @staticmethod
    def find_motherboard(
        filters: MotherboardFilters, count: int = COMPONENT_COUNT
    ) -> list[Motherboard]:
        """finds motherboards in DB"""
        filters = normalize_filters(filters)
        return MbRepo(db).find(filters, limit=count)

    # PSU
    @staticmethod
    def find_psu(
        filters: PsuFilters, count: int = COMPONENT_COUNT
    ) -> list[PowerSupply]:
        """finds power supplies in DB"""
        filters = normalize_filters(filters)
        return PsuRepo(db).find(filters, limit=count)
