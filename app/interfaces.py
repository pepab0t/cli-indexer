from typing import Protocol


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
