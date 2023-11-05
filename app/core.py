import os
import re
from pathlib import Path
from typing import Iterator, Callable, Generator, Protocol
from .exceptions import CLIIndexerException
from collections import defaultdict
from .entity import OutputInfo, Occurance
from .index import IndexDB, Index
from .interfaces import Insertable


def walk_files(root: Path) -> Iterator[Path]:
    for root_dir, _, files in filter(lambda item: len(item[2]) > 0, os.walk(root)):
        dir_path: Path = Path(root_dir)
        for file in files:
            yield (dir_path / file)


def walk(
    root: Path, predicate: Callable[[Path], bool] = lambda p: True
) -> Generator[Path, None, None]:
    for root_dir, dirs, files in os.walk(root):
        dir_path: Path = Path(root_dir)
        for file in files:
            if predicate(p := (dir_path / file)):
                yield p
        if not dirs:
            if predicate(dir_path):
                yield dir_path


REGEX_REPLACEMENTS = {"*", "[", "]", "?", "+", ".", "<", ">", "(", ")"}


def clean_regex(inform: str) -> str:
    for symbol in REGEX_REPLACEMENTS:
        inform = inform.replace(symbol, f"\\{symbol}")
    return inform


class Indexer:
    @staticmethod
    def make_index(root: Path, index: Insertable) -> None:
        if not root.is_dir():
            raise CLIIndexerException(f"{root} not a dir")
        for path in walk(root):
            try:
                index.insert(str(path), path.read_text(encoding="utf-8").splitlines())
            except Exception:
                pass


class SearchEngine:
    @staticmethod
    def search_information_index(
        information: str, index: Index
    ) -> Iterator[OutputInfo]:
        information = clean_regex(information)
        pattern = re.compile(f"{information}")

        for fpath, lines in index.files():
            occurances = {}
            for i, line in enumerate(lines, start=1):
                if pattern.search(line) is None:
                    continue

                spans = [m.span() for m in pattern.finditer(line)]

                occurances[i] = Occurance(line.rstrip(), spans)

            if len(occurances) > 0:
                yield OutputInfo(fpath, occurances)

    @staticmethod
    def search_information_index_db(info: str, index: IndexDB):
        data = defaultdict(list)
        info = clean_regex(info)

        pattern = re.compile(f"{info}")

        for item in index.select_information(info):
            data[item[0]].append((item[1], item[2]))

        for fpath, lines in data.items():
            occs: dict[int, Occurance] = {}
            for line, i in lines:
                occs[i] = Occurance(line, [m.span() for m in pattern.finditer(line)])
            yield OutputInfo(fpath, occs)

    @staticmethod
    def search_information_runtime(
        information: str, root: Path
    ) -> Iterator[OutputInfo]:
        if not root.is_dir():
            raise CLIIndexerException(f"{root} not a dir")

        information = clean_regex(information)
        pattern = re.compile(f"{information}")

        for fpath in walk_files(root):
            occurances = {}
            with fpath.open("r", encoding="utf-8") as f:
                try:
                    lines = f.readlines()
                except Exception:
                    continue

                for i, line in enumerate(lines, start=1):
                    if pattern.search(line) is None:
                        continue

                    spans = [m.span() for m in pattern.finditer(line)]
                    occurances[i] = Occurance(line.rstrip(), spans)
            if len(occurances):
                yield OutputInfo(str(fpath), occurances)

    @staticmethod
    def search_fd_index(name_part: str, index: Index) -> Iterator[OutputInfo]:
        name_part = clean_regex(name_part)
        pattern: re.Pattern = re.compile(f"{name_part}")

        for k in index.keys():
            if pattern.search(k) is None:
                continue

            spans = [m.span() for m in pattern.finditer(k)]

            yield OutputInfo(k, dict(), spans)

    @staticmethod
    def search_fd_runtime(name_part: str, root: Path) -> Iterator[OutputInfo]:
        if not root.is_dir():
            raise CLIIndexerException(f"{root} not a dir")
        name_part = clean_regex(name_part)
        pattern: re.Pattern = re.compile(f"{name_part}")

        for path in walk(root):
            path_str = str(path)
            if pattern.search(path_str) is None:
                continue

            spans = [m.span() for m in pattern.finditer(path_str)]

            yield OutputInfo(path_str, dict(), spans)

    @staticmethod
    def search_fdi_index(
        name_part: str, inform: str, index: Index
    ) -> Iterator[OutputInfo]:
        name_part = clean_regex(name_part)
        inform = clean_regex(inform)

        pattern_file: re.Pattern = re.compile(f"{name_part}")
        pattern_info: re.Pattern = re.compile(f"{inform}")

        for fpath, lines in index.files():
            if pattern_file.search(fpath) is None:
                continue

            occs: dict[int, Occurance] = {}
            for i, line in enumerate(lines, start=1):
                if pattern_info.search(line) is None:
                    continue
                occs[i] = Occurance(
                    line, [m.span() for m in pattern_info.finditer(line)]
                )

            if len(occs) == 0:
                continue

            yield OutputInfo(
                fpath, occs, [m.span() for m in pattern_file.finditer(fpath)]
            )

    @staticmethod
    def search_fdi_runtime(
        name_part: str, inform: str, root: Path
    ) -> Iterator[OutputInfo]:
        if not root.is_dir():
            raise CLIIndexerException(f"{root} not a dir")
        name_part = clean_regex(name_part)
        inform = clean_regex(inform)

        pattern_file: re.Pattern = re.compile(f"{name_part}")
        pattern_info: re.Pattern = re.compile(f"{inform}")

        for path in walk_files(root):
            path_str = str(path)
            if pattern_file.search(path_str) is None:
                continue

            occs: dict[int, Occurance] = {}
            try:
                lines = path.read_text().splitlines()
            except Exception:
                continue

            for i, line in enumerate(lines, start=1):
                if pattern_info.search(line) is None:
                    continue
                occs[i] = Occurance(
                    line, [m.span() for m in pattern_info.finditer(line)]
                )

            if len(occs) == 0:
                continue

            yield OutputInfo(
                path_str, occs, [m.span() for m in pattern_file.finditer(path_str)]
            )
