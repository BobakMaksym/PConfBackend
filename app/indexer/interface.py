from abc import ABC, abstractmethod
from typing import Any

from app.repos.search_repo import IIndexRepo


class IChangeHandler(ABC):
    @abstractmethod
    def __init__(self, repo: IIndexRepo): ...

    @abstractmethod
    def handle(self, change: Any) -> None: ...
