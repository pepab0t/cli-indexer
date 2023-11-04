from typing import Protocol, Iterator
from .abs import Command
from pathlib import Path
from ..exceptions import ArgumentException
from ..entity import Index, OutputInfo


class Engine(Protocol):
    def search_fd_index(self, name_part: str, index: Index) -> Iterator[OutputInfo]:
        ...

    def search_fd_runtime(self, name_part: str, root: Path) -> Iterator[OutputInfo]:
        ...


class SearchFileDirCommand(Command):
    name: str = "searchfd"
    doc: str = f"""
{name} name (root | -i index_file)
    Search files or directories
    - name: file or directory name to search
    - root: searching root directory
    - index_file:
        if not specified, autocreate index first
        if specified, use index file"""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

        self.name_key = "name"
        self.index_file_key = "index_file"
        self.root_key = "root"

    def parse_args(self, args: list[str]):
        out = {}

        match args:
            case [name, root]:
                out[self.name_key] = name
                out[self.root_key] = Path(root)
            case [name, "-i", index_file]:
                out[self.name_key] = name
                out[self.index_file_key] = Path(index_file)
            case _:
                raise ArgumentException("invalid arguments")

        return out

    def execute(self, args: list[str]) -> None:
        parsed = self.parse_args(args)

        if (index_path := parsed.get(self.index_file_key)) is not None:
            index: Index = Index.load(index_path)
            it = self.engine.search_fd_index(parsed[self.name_key], index)
        else:
            root: Path = parsed[self.root_key]
            it = self.engine.search_fd_runtime(parsed[self.name_key], root)

        c: bool = False
        for out in it:
            print(out.format(), end="")
            c = True

        if not c:
            print("nothing found")
