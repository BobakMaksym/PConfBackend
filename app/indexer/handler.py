import logging

from typesense import exceptions as e

from app.indexer.interface import IChangeHandler
from app.repos.search_repo import SearchSchema
from app.indexer.repo import IIndexRepo
from app.schemas.change_stream_schema import ChangeStreamSchema


logger = logging.getLogger(__name__)


class DeleteHandler(IChangeHandler):
    def __init__(self, repo: IIndexRepo):
        self.repo = repo

    def handle(self, change: ChangeStreamSchema):
        id = change.id
        coll = change.ns.coll

        try:
            self.repo.delete(coll, id)
            logger.info("delete %s in %s", str(id), coll)
        except e.ObjectNotFound:
            logger.info("tried to delete %s in %s, but document not found")


class UpdateHandler(IChangeHandler):
    def __init__(self, repo: IIndexRepo):
        self.repo = repo

    def handle(self, change: ChangeStreamSchema):

        if not change.update_description:
            return

        try:
            model = change.update_description["updatedFields"]["model"]
        except:
            return

        id = change.id
        coll = change.ns.coll

        document = SearchSchema(id=id, model=model)

        self.repo.upsert(coll, document)

        logger.info("upsert %s in %s", str(id), coll)


class InsertHandler(IChangeHandler):
    def __init__(self, repo: IIndexRepo):
        self.repo = repo

    def handle(self, change: ChangeStreamSchema):
        if not change.full_document:
            return

        id = change.id
        coll = change.ns.coll

        document = SearchSchema(id=id, model=change.full_document["model"])

        self.repo.upsert(coll, document)

        logger.info("insert* or update %s in %s", str(id), coll)
