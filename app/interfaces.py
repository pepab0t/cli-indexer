from typing import Protocol


class Insertable(Protocol):
    def insert(self, path: str, lines: list[str]) -> None:
        ...
