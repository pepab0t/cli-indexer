import sqlite3
from pathlib import Path
import pickle
from typing import Generator, Iterator
from .exceptions import CLIIndexerException
from datetime import datetime


class IndexDB:
    def __init__(self, db_name: Path):
        if db_name.suffix not in {".db", ".sqlite"}:
            raise CLIIndexerException(f"expected {db_name} to be .db or .sqlite file")

        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS paths (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            path TEXT NOT NULL UNIQUE
        );"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS lines (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            line TEXT NOT NULL,
                            path_id INTEGER NOT NULL,
                            line_n INTEGER NOT NULL,
                            FOREIGN KEY (path_id) REFERENCES paths (id)
        );"""
        )

    def select_information(self, information: str) -> list[tuple[str, str, int]]:
        self.cursor.execute(
            f"""SELECT paths.path, lines.line, lines.line_n 
            FROM lines JOIN paths ON paths.id=lines.path_id 
            WHERE lines.line LIKE '%{information}%'"""
        )

        return self.cursor.fetchall()

    def insert(self, path: str, lines: list[str]):
        self.cursor.execute("INSERT INTO paths (path) VALUES (?)", (path,))
        path_id = self.cursor.lastrowid
        self.cursor.executemany(
            "INSERT INTO lines (line, path_id, line_n) VALUES (?, ?, ?)",
            ((line, path_id, i) for i, line in enumerate(lines, start=1)),
        )

    def __del__(self):
        try:
            self.connection.commit()
            del self.cursor
            self.connection.close()
        except Exception:
            pass


class Index:
    def __init__(self, dst: Path):
        if not self.valid_pkl(dst):
            raise CLIIndexerException(f"Expected {dst} to be .pkl file")

        self.created: str = datetime.now().strftime(r"%d.%m.%Y %H:%M:%S")
        self._d: dict[str, list[str] | None] = {}
        self.dst = dst

    def insert(self, path: str, lines: list[str]):
        if not lines:
            self._d[path] = None
        else:
            self._d[path] = lines

    def dump(self):
        if self._d is None:
            raise CLIIndexerException("Empty data, nothing to dump.")
        with self.dst.open("wb") as f:
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
            raise CLIIndexerException(f"No such file {fpath}")
        with fpath.open("rb") as f:
            try:
                obj = pickle.load(f)
            except Exception:
                raise CLIIndexerException(f"Cannot load `{fpath}`, may be damaged.")

        if not isinstance(obj, Index):
            raise CLIIndexerException(
                f"Wrong object of type {obj.__class__.__name__} (expected {Index.__name__})"
            )
        return obj
