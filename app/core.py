import os
import re
from pathlib import Path
from typing import Iterator, Callable, Generator
from .exceptions import IndexerException
from collections import defaultdict
from .entity import Index, OutputInfo, Occurance


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
    def make_index(root: Path) -> Index:
        if not root.is_dir():
            raise IndexerException(f"{root} not a dir")
        index = Index()
        for path in walk(root):
            try:
                index.add(str(path), path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return index


class SearchEngine:
    @staticmethod
    def search_information_index(
        information: str, index: Index
    ) -> Iterator[OutputInfo]:
        information = clean_regex(information)
        pattern = re.compile(f"{information}")

        for fpath, lines in index.files():
            occurances = defaultdict(list)
            for i, line in enumerate(lines, start=1):
                if pattern.search(line) is None:
                    continue

                spans = [m.span() for m in pattern.finditer(line)]

                occ = Occurance(line.rstrip(), spans)
                occurances[i].append(occ)

            if len(occurances) > 0:
                yield OutputInfo(fpath, occurances)

    @staticmethod
    def search_information_runtime(
        information: str, root: Path
    ) -> Iterator[OutputInfo]:
        if not root.is_dir():
            raise IndexerException(f"{root} not a dir")

        information = clean_regex(information)
        pattern = re.compile(f"{information}")

        for fpath in walk_files(root):
            occurances = defaultdict(list)
            with fpath.open("r", encoding="utf-8") as f:
                if fpath.name == "file_gpodilao..ext":
                    print(end="")
                try:
                    lines = f.readlines()
                except Exception:
                    continue

                for i, line in enumerate(lines, start=1):
                    if pattern.search(line) is None:
                        continue

                    spans = [m.span() for m in pattern.finditer(line)]
                    occurances[i].append(Occurance(line.rstrip(), spans))
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
            raise IndexerException(f"{root} not a dir")
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

            occs = defaultdict(list)
            for i, line in enumerate(lines, start=1):
                if pattern_info.search(line) is None:
                    continue

                occ = Occurance(line, [m.span() for m in pattern_info.finditer(line)])
                occs[i].append(occ)

            if len(occs) == 0:
                continue

            yield OutputInfo(
                fpath, occs, [m.span() for m in pattern_file.finditer(fpath)]
            )
