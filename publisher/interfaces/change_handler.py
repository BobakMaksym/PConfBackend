from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel

    from schemas import Change


class IChangeHandler(ABC):
    @abstractmethod
    def handle(
        self,
        change: "Change",
        channel: "BlockingChannel",
    ): ...
