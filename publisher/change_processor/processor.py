from typing import TYPE_CHECKING

from interfaces import IChangeProcessor

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel

    from enums import Operation
    from interfaces import IChangeHandler
    from schemas import Change


class ChangeProcessor(IChangeProcessor):
    def __init__(
        self,
        handlers: dict["Operation", "IChangeHandler"],
        channel: "BlockingChannel",
    ):
        self._handlers = handlers
        self._channel = channel

    def process(self, change: "Change"):
        handler = self._handlers[change.operation_type]
        handler.handle(change=change, channel=self._channel)
