import logging
from typing import TYPE_CHECKING

from interfaces import IChangeHandler

if TYPE_CHECKING:
    from schemas import Change


logger = logging.getLogger(__name__)


def test_log(change: "Change"):
    logger.info("\n%s", change.model_dump_json())


class DeleteHandler(IChangeHandler):

    def handle(self, change: "Change"):
        id, coll = change.id, change.ns.coll
        test_log(change)
        pass


class UpdateHandler(IChangeHandler):

    def handle(self, change: "Change"):
        id, coll = change.id, change.ns.coll
        test_log(change)
        pass


class InsertHandler(IChangeHandler):

    def handle(self, change: "Change"):
        id, coll = change.id, change.ns.coll
        test_log(change)
        pass
