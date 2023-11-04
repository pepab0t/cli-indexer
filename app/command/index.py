from typing import Protocol
from .abs import Command
from ..exceptions import ArgumentException, IndexerException
from pathlib import Path
from ..entity import FileIndex


class Indexer(Protocol):
    def make_index(self, root: Path) -> None:
        ...

    def dump_data(self, dst: Path) -> None:
        ...


class IndexCommand(Command):
    name: str = "index"
    doc: str = """
index root_dir [-o output_file]
    Create index for root_dir
    - root_dir: directory to index
    - output_file: path to output file
        must be .pkl file
        default ./index.pkl"""

    default_dst = Path("./index.pkl")

    def __init__(self, indexer: Indexer):
        self.indexer = indexer

        self.root_dir_key = "root_dir"
        self.output_file_key = "output_file"

    def parse_args(self, args: list[str]):
        match args:
            case [root_dir]:
                return {self.root_dir_key: Path(root_dir)}
            case [root_dir, "-o", output_file]:
                return {
                    self.root_dir_key: Path(root_dir),
                    self.output_file_key: Path(output_file),
                }
            case _:
                raise ArgumentException("invalid arguments")

    def execute(self, args: list[str]) -> None:
        parsed = self.parse_args(args)
        dst: Path = parsed.get(self.output_file_key, self.default_dst)

        if not FileIndex.valid_pkl(dst):
            raise IndexerException(f"File {dst} is not valid .pkl file")

        self.indexer.make_index(parsed[self.root_dir_key])
        self.indexer.dump_data(dst)

        print(f"Created index file: {dst}")
