from typing import TYPE_CHECKING

from interfaces import IChangeProcessor

if TYPE_CHECKING:
    from enums import Operation
    from interfaces import IChangeHandler
    from schemas import Change


class ChangeProcessor(IChangeProcessor):
    def __init__(self, handlers: dict["Operation", "IChangeHandler"]):
        self._handlers = handlers

    def process(self, change: "Change"):
        handler = self._handlers[change.operation_type]
        handler.handle(change)
