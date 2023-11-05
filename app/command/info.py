from typing import Protocol, Iterable
from .abs import Command
from ..exceptions import ArgumentException
from ..entity import OutputInfo
from pathlib import Path
from ..index import Index, IndexDB


class Engine(Protocol):
    def search_runtime(self, information: str, root: Path) -> Iterable[OutputInfo]:
        ...

    def search_index(self, information: str, index: Index) -> Iterable[OutputInfo]:
        ...


class SearchInfoCommand(Command):
    name: str = "info"
    doc: str = f"""
{name} inform (root_dir | -i index_file)
    Find information within files
    - inform: information to find
    - root_dir: directory to search
    - index_file:
        if not specified, autocreate index first (more runtime required)
        if specified, use index file"""

    def __init__(self, engine: Engine):
        self.engine = engine

        self.info_key = "info"
        self.root_dir_key = "root_dir"
        self.index_file_key = "index_file_key"

    def parse_args(self, args: list[str]):
        output = {}
        match args:
            case [info, root_dir]:
                output[self.info_key] = info
                output[self.root_dir_key] = Path(root_dir)
            case [info, "-i", index_file]:
                output[self.info_key] = info
                output[self.index_file_key] = Path(index_file)
            case _:
                raise ArgumentException("invalid arguments")
        return output

    def execute(self, args: list[str]) -> None:
        parsed = self.parse_args(args)

        info: str = parsed[self.info_key]

        if (root := parsed.get(self.root_dir_key)) is not None:
            print(f"Finding information runtime")
            it = self.engine.search_runtime(info, root)
        else:
            # index = IndexDB(parsed[self.index_file_key])
            index = Index.load(parsed[self.index_file_key])
            print(f"Loaded index from: {index.created}")
            it = self.engine.search_index(info, index)

        count = 0
        for item in it:
            print(item.format())
            count += 1

        if count == 0:
            print("nothing found")
