from typing import Protocol, Iterable
from .abs import Command
from ..exceptions import ArgumentException
from ..entity import OutputInfo, InfoIndex
from pathlib import Path


class Indexer(Protocol):
    def search_information_runtime(
        self, information: str, root: Path
    ) -> Iterable[OutputInfo]:
        ...

    def search_information_index(
        self, information: str, index: InfoIndex
    ) -> Iterable[OutputInfo]:
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

        info: str = parsed[self.info_key]

        if (root := parsed.get(self.root_dir_key)) is not None:
            print(f"Finding information runtime")
            it = self.indexer.search_information_runtime(info, root)
        else:
            index = InfoIndex.load(parsed[self.index_file_key])
            print(f"Loaded index from: {index.created}")
            it = self.indexer.search_information_index(info, index)

        count = 0
        for item in it:
            print(item.format())
            count += 1

        if count == 0:
            print("nothing found")
