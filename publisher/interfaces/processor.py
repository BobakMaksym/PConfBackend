from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enums import Operation
    from schemas import Change
    from interfaces.change_handler import IChangeHandler


class IChangeProcessor:
    def __init__(
        self,
        handlers: dict["Operation", "IChangeHandler"],
    ) -> None: ...

    def process(self, change: "Change") -> None: ...
