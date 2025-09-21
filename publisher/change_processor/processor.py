from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel

    from enums import Operation
    from change_processor import IChangeHandler
    from schemas import Change


class IChangeProcessor:
    def __init__(
        self,
        handlers: dict["Operation", "IChangeHandler"],
        channel: "BlockingChannel",
    ) -> None: ...

    def process(self, change: "Change") -> None: ...


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
