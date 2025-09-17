from abc import ABC, abstractmethod
from typing import Any

from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.repos.component_repo import IComponentRepo
from app.repos.search_repo import (
    SearchSchema,
    IIndexRepo,
    CpuIndexRepo,
    GpuIndexRepo,
    RamIndexRepo,
    PsuIndexRepo,
    MotherboardIndexRepo,
)
from app.repos.component_repo import (
    CpuRepo,
    RamRepo,
    GpuRepo,
    PsuRepo,
    MbRepo,
)


class IIndexSyncService(ABC):
    @abstractmethod
    def __init__(self, db_repo: IComponentRepo, index_repo: IIndexRepo): ...

    @abstractmethod
    def upsert(self, doc: SearchSchema): ...

    @abstractmethod
    def delete(self, id: MongoObjectId): ...

    @abstractmethod
    def sync_all(self) -> dict[str, Any]: ...


class BaseComponentIndexSyncService(IIndexSyncService):
    def __init__(self, db_repo: IComponentRepo, index_repo: IIndexRepo):
        self.db_repo = db_repo
        self.index_repo = index_repo

    def upsert(self, doc):
        self.index_repo.upsert_doc(doc)

    def delete(self, id):
        self.index_repo.delete_doc(id)

    def sync_all(self):
        documents = self.db_repo.get_all()

        doc_inserted_count = 0
        for doc in documents:
            search_doc = SearchSchema.model_validate(doc)
            self.index_repo.upsert_doc(search_doc)

            doc_inserted_count += 1

        return {"inserted": doc_inserted_count}


class CpuIndexSyncService(BaseComponentIndexSyncService):
    def __init__(self, db_repo: CpuRepo, index_repo: CpuIndexRepo):
        super().__init__(db_repo=db_repo, index_repo=index_repo)


class GpuIndexSyncService(BaseComponentIndexSyncService):
    def __init__(self, db_repo: GpuRepo, index_repo: GpuIndexRepo):
        super().__init__(db_repo=db_repo, index_repo=index_repo)


class RamIndexSyncService(BaseComponentIndexSyncService):
    def __init__(self, db_repo: RamRepo, index_repo: RamIndexRepo):
        super().__init__(db_repo=db_repo, index_repo=index_repo)


class PsuIndexSyncService(BaseComponentIndexSyncService):
    def __init__(self, db_repo: PsuRepo, index_repo: PsuIndexRepo):
        super().__init__(db_repo=db_repo, index_repo=index_repo)


class MotherboardIndexSyncService(BaseComponentIndexSyncService):
    def __init__(self, db_repo: MbRepo, index_repo: MotherboardIndexRepo):
        super().__init__(db_repo=db_repo, index_repo=index_repo)


class TsCollectionInitializer:
    def __init__(self, *index_repo: IIndexRepo):
        self.index_repos = index_repo

    def init_all(self):
        for repo in self.index_repos:
            repo.init_collection()

    def drop_all(self):
        for repo in self.index_repos:
            repo.drop_collection()
