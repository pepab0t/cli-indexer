import os
import re
from pathlib import Path
from typing import Iterator
from .exceptions import IndexerException
from collections import defaultdict
from .entity import FileIndex, OutputInfo, Occurance


def walk_files(root: Path) -> Iterator[Path]:
    for root_dir, _, files in filter(lambda item: len(item[2]) > 0, os.walk(root)):
        dir_path: Path = Path(root_dir)
        for file in files:
            yield (dir_path / file)


REGEX_REPLACEMENTS = {"*", "[", "]", "?", "+", ".", "<", ">", "(", ")", "-", "="}


def prepare_information(inform: str) -> str:
    for symbol in REGEX_REPLACEMENTS:
        inform = inform.replace(symbol, f"\\{symbol}")
    return inform


class Indexer:
    def __init__(self):
        self.data: FileIndex | None = None

    def make_index(self, root: Path):
        self.data = FileIndex()
        if not root.is_dir():
            raise IndexerException(f"{root} not a dir")
        for file in walk_files(root):
            try:
                self.data.add(str(file), file.read_text(encoding="utf-8"))
            except Exception:
                pass

    def get_datetime(self) -> str:
        if self.data is None:
            raise IndexerException("missing datm")

        return self.data.created

    def dump_data(self, dst: Path):
        if self.data is not None:
            self.data.dump(dst)

    def load_data(self, fpath: Path):
        self.data = FileIndex.load(fpath)

    def search_information(self, information: str) -> list[OutputInfo]:
        if self.data is None:
            raise IndexerException("No data loaded")

        information = prepare_information(information)

        pattern = re.compile(f"{information}")
        outputs: list[OutputInfo] = []

        for fpath, lines in self.data.items():
            occurances = defaultdict(list)
            for i, line in enumerate(lines, start=1):
                if pattern.search(line) is None:
                    continue

                spans: list[tuple[int, int]] = []
                for m in pattern.finditer(line):
                    spans.append(m.span())

                occ = Occurance(line, spans)
                occurances[i].append(occ)

            if len(occurances) > 0:
                output_info = OutputInfo(fpath, occurances)
                outputs.append(output_info)

        return outputs
