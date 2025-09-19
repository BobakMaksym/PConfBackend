from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel

    from enums import Operation
    from schemas import Change
    from interfaces.change_handler import IChangeHandler


class IChangeProcessor:
    def __init__(
        self,
        handlers: dict["Operation", "IChangeHandler"],
        channel: "BlockingChannel",
    ) -> None: ...

    def process(self, change: "Change") -> None: ...
