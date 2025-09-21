from abc import ABC, abstractmethod
import logging
from typing import TYPE_CHECKING

from schemas import IndexDoc

if TYPE_CHECKING:
    from index.index_repo import IIndex
    from schemas import Change


logger = logging.getLogger(__name__)


class IIndexChangeHandler(ABC):
    @abstractmethod
    def __init__(self, index_repo: "IIndex"): ...

    @abstractmethod
    def handle(self, change: "Change"): ...


class BaseIndexHandler(IIndexChangeHandler):
    def __init__(self, index_repo: "IIndex"):
        self.index_repo = index_repo


class IndexDeleteHandler(BaseIndexHandler):

    def handle(self, change: "Change"):
        id, coll = change.id, change.ns.coll
        self.index_repo.delete(collection=coll, id=id)


class IndexUpdateHandler(BaseIndexHandler):

    def handle(self, change: "Change"):
        new_doc = IndexDoc(**change.full_document)
        self.index_repo.upsert(collection=change.ns.coll, doc=new_doc)


class IndexInsertHandler(BaseIndexHandler):

    def handle(self, change: "Change"):
        new_doc = IndexDoc(**change.full_document)
        self.index_repo.upsert(collection=change.ns.coll, doc=new_doc)
