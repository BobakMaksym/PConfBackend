from typing import TYPE_CHECKING, Iterable
from logging import getLogger

from typesense.types.collection import CollectionCreateSchema

from app.core.configs.typesense_config import ComponentType
from app.repos.index_repo import SearchIndexRepo
from app.schemas.index_schema import IndexSchema

if TYPE_CHECKING:
    from app.repos.component_repo import IComponentRepo


logger = getLogger("app")


class SyncSearchIndex:
    def __init__(
        self,
        db_repos: dict[str, "IComponentRepo"],
        index_repo: SearchIndexRepo,
        coll_schemas: dict[ComponentType, CollectionCreateSchema],
    ):
        self._db_repos = db_repos
        self._index_repo = index_repo
        self._coll_schemas = coll_schemas

    def create_coll_all(self, collections: Iterable[str] = ComponentType):
        """
        creates collections for all types of components in the index
        """
        for coll in collections:
            self._index_repo.create(self._coll_schemas[coll])

    def sync_coll(self, coll: ComponentType):
        """
        synchronizes data in specific collection
        """
        component_repo = self._db_repos[coll]()

        db_docs = component_repo.get_all()

        index_docs = [IndexSchema.model_validate(doc) for doc in db_docs]

        self._index_repo.add_all_docs_to_coll(coll=coll, docs=index_docs)

    def sync_coll_all(self, collections: Iterable[str] = ComponentType):
        """
        synchronizes data across all collections
        """
        for coll in collections:
            self.sync_coll(coll=coll)

    def drop_all(self, collections: Iterable[str] = ComponentType):
        """
        deletes all collection and data
        """
        for coll in collections:
            self._index_repo.drop(coll=coll)
