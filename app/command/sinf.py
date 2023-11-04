from typing import Protocol
from .abs import Command
from ..exceptions import ArgumentException
from ..entity import OutputInfo
from pathlib import Path


class Indexer(Protocol):
    def make_index(self, root: Path) -> None:
        ...

    def load_data(self, fpath: Path) -> None:
        ...

    def search_information(self, information: str) -> list[OutputInfo]:
        ...

    def get_datetime(self) -> str:
        ...


class SearchInfoCommand(Command):
    name: str = "sinf"
    doc: str = """
sinf info (root_dir | -i index_file)
    Find information within files
    - info: information to find
    - root_dir: directory to search
    - index_file:
        if not specified, autocreate index first (more runtime required)
        if specified, use index file"""

    def __init__(self, indexer: Indexer):
        self.indexer = indexer

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

        if (root := parsed.get(self.root_dir_key)) is not None:
            print(f"Creating index for dir: {root}")
            self.indexer.make_index(root)
        else:
            self.indexer.load_data(parsed[self.index_file_key])
            print(f"Loaded index from: {self.indexer.get_datetime()}")

        out = self.indexer.search_information(parsed[self.info_key])

        if out:
            for o in out:
                print(o.format())
        else:
            print("nothing found")
