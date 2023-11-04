from typing import Protocol
from .abs import Command


class Indexer(Protocol):
    pass


class SearchFileDirCommand(Command):
    name: str = "sfd"
    doc: str = """
sfd name [-i index_file]
    Search files or directories
    - name: file or directory name to search
    - index_file:
        if not specified, autocreate index first
        if specified, use index file"""

    def __init__(self, indexer: Indexer) -> None:
        self.indexer = indexer

    def execute(self) -> None:
        return super().execute()
