from datetime import datetime
from pathlib import Path
from .exceptions import CLIIndexerException
import pickle
from typing import Generator, Callable, Iterator
from .colors import red_text, blue_text, green_text
from dataclasses import dataclass, field


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
    occurances: dict[int, Occurance]
    fpath_spans: list[tuple[int, int]] = field(default_factory=list)

    def format_fpath(self):
        return color_text(self.fpath, green_text, self.fpath_spans)

    def format(self) -> str:
        output = green_text("Path: ") + self.format_fpath() + "\n"
        for line_num, occ in self.occurances.items():
            # for occ in occurances:
            output += f"\t{blue_text(f'Line {line_num}')}: {occ.format()}\n"
        return output
