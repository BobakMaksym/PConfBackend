from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from index.handlers import IHandler
    from enums import Operation
    from schemas import Change


logger = logging.getLogger(__name__)


class ChangeProcessor:
    def __init__(
        self,
        handlers: dict["Operation", "IHandler"],
    ):
        self._handlers = handlers

    def process(self, change: "Change"):
        handler = self._handlers[change.operation_type]
        handler.handle(change=change)
