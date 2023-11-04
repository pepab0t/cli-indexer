import os
import re
from pathlib import Path
from typing import Iterator, Callable, Generator
from .exceptions import IndexerException
from collections import defaultdict
from .entity import InfoIndex, OutputInfo, Occurance


def walk_files(root: Path) -> Iterator[Path]:
    for root_dir, _, files in filter(lambda item: len(item[2]) > 0, os.walk(root)):
        dir_path: Path = Path(root_dir)
        for file in files:
            yield (dir_path / file)


def walk(root: Path, predicate: Callable[[Path], bool]):
    for root_dir, _, files in os.walk(root):
        dir_path: Path = Path(root_dir)
        if files:
            for file in files:
                if predicate(p := (dir_path / file)):
                    yield p
        else:
            if predicate(dir_path):
                yield dir_path


REGEX_REPLACEMENTS = {"*", "[", "]", "?", "+", ".", "<", ">", "(", ")", "-", "="}


def prepare_information(inform: str) -> str:
    for symbol in REGEX_REPLACEMENTS:
        inform = inform.replace(symbol, f"\\{symbol}")

    return inform


class Indexer:
    @staticmethod
    def make_index(root: Path) -> InfoIndex:
        if not root.is_dir():
            raise IndexerException(f"{root} not a dir")
        index = InfoIndex()
        for file in walk_files(root):
            try:
                index.add(str(file), file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return index

    @staticmethod
    def search_information_index(
        information: str, index: InfoIndex
    ) -> Iterator[OutputInfo]:
        information = prepare_information(information)
        pattern = re.compile(f"{information}")

        for fpath, lines in index.items():
            occurances = defaultdict(list)
            for i, line in enumerate(lines, start=1):
                if pattern.search(line) is None:
                    continue

                spans = [m.span() for m in pattern.finditer(line)]

                occ = Occurance(line, spans)
                occurances[i].append(occ)

            if len(occurances) > 0:
                yield OutputInfo(fpath, occurances)

    @staticmethod
    def search_information_runtime(
        information: str, root: Path
    ) -> Iterator[OutputInfo]:
        if not root.is_dir():
            raise IndexerException(f"{root} not a dir")

        information = prepare_information(information)
        pattern = re.compile(f"{information}")

        for fpath in walk_files(root):
            occurances = defaultdict(list)
            with fpath.open("r", encoding="utf-8") as f:
                for i, line in enumerate(f, start=1):
                    if pattern.search(line) is None:
                        continue

                    spans = [m.span() for m in pattern.finditer(line)]
                    occurances[i].append(Occurance(line, spans))
            if len(occurances):
                yield OutputInfo(str(fpath), occurances)
