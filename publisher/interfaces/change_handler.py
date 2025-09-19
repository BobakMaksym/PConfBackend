from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas import Change


class IChangeHandler(ABC):
    @abstractmethod
    def handle(self, change: "Change"): ...
