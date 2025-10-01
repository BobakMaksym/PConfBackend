from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.repos.component_repo import IComponentRepo
    from app.repos.index_repo import IComponentIndexRepo


class SyncSearchIndexUseCase:
    def __init__(self, repos: list[tuple["IComponentRepo", "IComponentIndexRepo"]]):
        self.repos = repos

    def create_collections(self):
        for _, index_repo in self.repos:
            index_repo.create()

    def drop_collections(self):
        for _, index_repo in self.repos:
            index_repo.drop()

    def sync_data(self):
        for data_repo, index_repo in self.repos:
            docs = data_repo.get_all()
            index_repo.add_all_docs_to_coll(docs)
