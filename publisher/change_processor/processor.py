from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enums import Operation
    from change_processor import IChangeHandler
    from schemas import Change


class IChangeProcessor:
    def __init__(
        self,
        handlers: dict["Operation", "IChangeHandler"],
    ) -> None: ...

    def process(self, change: "Change") -> None: ...


class ChangeProcessor(IChangeProcessor):
    def __init__(
        self,
        handlers: dict["Operation", "IChangeHandler"],
    ):
        self._handlers = handlers

    def process(self, change: "Change"):
        handler = self._handlers[change.operation_type]
        handler.handle(change=change)
