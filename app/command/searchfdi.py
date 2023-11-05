from .abs import Command
from typing import Protocol, Iterator
from ..entity import OutputInfo
from ..exceptions import ArgumentException
from pathlib import Path
from ..index import Index


class Engine(Protocol):
    def search_fdi_index(
        self, name_part: str, inform: str, index: Index
    ) -> Iterator[OutputInfo]:
        ...

    def search_fdi_runtime(
        self, name_part: str, inform: str, root: Path
    ) -> Iterator[OutputInfo]:
        ...


class SearchFileDirInfoCommand(Command):
    name: str = "searchfdi"
    doc: str = f"""
{name} info name (root | -i index_file)
    Search information within specified file or directory
    - info: information to search for
    - name: name (can be part of the path) where information should be found
    - root: searhing root path
    - index_file: path to the index file
"""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def parse_args(self, args: list[str]):
        out = {}

        match args:
            case [info, name, root]:
                out["info"] = info
                out["name"] = name
                out["root"] = Path(root)
            case [info, name, "-i", index_file]:
                out["info"] = info
                out["name"] = name
                out["index"] = Path(index_file)
            case _:
                raise ArgumentException("invalid arguments")

        return out

    def execute(self, args: list[str]) -> None:
        parsed = self.parse_args(args)

        root = parsed.get("root")
        info = parsed["info"]
        name = parsed["name"]

        if root is not None:
            it = self.engine.search_fdi_runtime(name, info, root)
        else:
            it = self.engine.search_fdi_index(name, info, Index.load(parsed["index"]))

        c: bool = False
        for out in it:
            print(out.format(), end="")
            c = True

        if not c:
            print("nothing found")
