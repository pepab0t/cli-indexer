from datetime import datetime
from pathlib import Path
from .exceptions import IndexerException
import pickle
from typing import Generator, Callable, Iterator
from .colors import red_text, blue_text, green_text
from dataclasses import dataclass, field


class Index:
    def __init__(self):
        self.created: str = datetime.now().strftime(r"%d.%m.%Y %H:%M:%S")
        self._d: dict[str, list[str] | None] = {}

    def add(self, path: str, content: str | None):
        if content is None:
            self._d[path] = None
        else:
            self._d[path] = content.splitlines()

    def dump(self, dst: Path):
        if self._d is None:
            raise IndexerException("Empty data, nothing to dump.")
        if not self.valid_pkl(dst):
            raise IndexerException(f"Expected {dst} to be .pkl file")
        with dst.open("wb") as f:
            pickle.dump(self, f)

    def files(self) -> Generator[tuple[str, list[str]], None, None]:
        for k, v in self._d.items():
            if v is None:
                continue
            yield (k, v)

    def items(self) -> Generator[tuple[str, list[str] | None], None, None]:
        for item in self._d.items():
            yield item

    def keys(self) -> Iterator[str]:
        for k in self._d.keys():
            yield k

    @staticmethod
    def valid_pkl(fpath: Path):
        return fpath.suffix == ".pkl"

    @staticmethod
    def load(fpath: Path) -> "Index":
        if not fpath.is_file():
            raise IndexerException(f"No such file {fpath}")
        with fpath.open("rb") as f:
            try:
                obj = pickle.load(f)
            except Exception:
                raise IndexerException(f"Cannot load `{fpath}`, may be damaged.")

        if not isinstance(obj, Index):
            raise IndexerException(
                f"Wrong object of type {obj.__class__.__name__} (expected {Index.__name__})"
            )
        return obj


def color_text(
    text: str, color_fn: Callable[[str], str], spans: list[tuple[int, int]]
) -> str:
    output = ""
    start = 0
    for occ in spans:
        output += text[start : occ[0]] + color_fn(text[occ[0] : occ[1]])
        start = occ[1]

    output += text[start:]

    return output


@dataclass(frozen=True)
class Occurance:
    line: str
    indexes: list[tuple[int, int]]

    def format(self) -> str:
        return color_text(self.line, red_text, self.indexes)


@dataclass
class OutputInfo:
    fpath: str
    occurances: dict[int, list[Occurance]]
    fpath_spans: list[tuple[int, int]] = field(default_factory=list)

    def format_fpath(self):
        return color_text(self.fpath, green_text, self.fpath_spans)

    def format(self) -> str:
        output = green_text("Path: ") + self.format_fpath() + "\n"
        for line_num, occurances in self.occurances.items():
            for occ in occurances:
                output += f"\t{blue_text(f'Line {line_num}')}: {occ.format()}\n"
        return output
