from datetime import datetime
from pathlib import Path
from .exceptions import IndexerException
import pickle
from typing import Generator
from .colors import red_text, blue_text, green_text
from dataclasses import dataclass


class InfoIndex:
    def __init__(self):
        self.created: str = datetime.now().strftime(r"%d.%m.%Y %H:%M:%S")
        self._d: dict[str, list[str]] = {}

    def add(self, fpath: str, content: str):
        self._d[fpath] = content.splitlines()

    def dump(self, dst: Path):
        if self._d is None:
            raise IndexerException("Empty data, nothing to dump.")
        if not self.valid_pkl(dst):
            raise IndexerException(f"Expected {dst} to be .pkl file")
        with dst.open("wb") as f:
            pickle.dump(self, f)

    def items(self) -> Generator[tuple[str, list[str]], None, None]:
        for k, v in self._d.items():
            yield (k, v)

    @staticmethod
    def valid_pkl(fpath: Path):
        return fpath.suffix == ".pkl"

    @staticmethod
    def load(fpath: Path) -> "InfoIndex":
        if not fpath.is_file():
            raise IndexerException(f"No such file {fpath}")
        with fpath.open("rb") as f:
            obj = pickle.load(f)

        if not isinstance(obj, InfoIndex):
            raise IndexerException(
                f"Wrong object of type {obj.__class__.__name__} (expected {InfoIndex.__name__})"
            )
        return obj


@dataclass(frozen=True)
class Occurance:
    line: str
    indexes: list[tuple[int, int]]

    def format(self) -> str:
        output = ""
        start = 0
        for occ in self.indexes:
            output += self.line[start : occ[0]] + red_text(self.line[occ[0] : occ[1]])
            start = occ[1]

        output += self.line[start:]

        return output


@dataclass
class OutputInfo:
    fpath: str
    occurances: dict[int, list[Occurance]]

    def format(self) -> str:
        output = green_text("File: ") + self.fpath + "\n"
        for line_num, occurances in self.occurances.items():
            for occ in occurances:
                output += f"\t{blue_text(f'Line {line_num}')}: {occ.format()}\n"
        return output
