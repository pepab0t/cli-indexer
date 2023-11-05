from typing import Protocol, Any
from abc import ABC, abstractmethod


class Insertable(Protocol):
    def insert(self, path: str, lines: list[str]) -> None:
        ...


class Executable(Protocol):
    @property
    def name(self) -> str:
        ...

    @property
    def doc(self) -> str:
        ...

    def execute(self, args: list[str] = list()) -> None:
        ...


class SearchEngine(ABC):
    def search_index(self, *args, **kwargs) -> Any:
        ...

    def search_runtime(self, *args, **kwargs) -> Any:
        ...
