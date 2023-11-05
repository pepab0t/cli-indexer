#!/usr/bin/env python3
from app import (
    Indexer,
    CLIApplication,
    SearchInfoEngine,
    SearchFileDirEngine,
    SearchFileDirInfoEngine,
)
from app.command import (
    IndexCommand,
    SearchFileDirCommand,
    SearchInfoCommand,
    SearchFileDirInfoCommand,
)
import sys


def main():
    indexer = Indexer()
    si_engine = SearchInfoEngine()
    sfd_engine = SearchFileDirEngine()
    sfdi_engine = SearchFileDirInfoEngine()

    # sys.argv = ["main.py", "index", "."]
    # sys.argv = ["main.py", "info", "xxx", "."]
    # sys.argv = ["main.py", "info", "xxx", "-i", "index.pkl"]
    # sys.argv = ["main.py", "searchfd", "ewmyj", "-i", "index.pkl"]
    # sys.argv = ["main.py", "searchfd", "ewmyj", "."]
    # sys.argv = ["main.py", "searchfdi", "xxx", "..ext", "-i", "index.pkl"]
    # sys.argv = ["main.py", "searchfdi", "xxx", "..ext", "."]
    # sys.argv = ["main.py", "searchfdi", "ext", "-i", "i.pkl"]

    cli = CLIApplication()
    cli.register_command(IndexCommand(indexer))
    cli.register_command(SearchInfoCommand(si_engine))
    cli.register_command(SearchFileDirCommand(sfd_engine))
    cli.register_command(SearchFileDirInfoCommand(sfdi_engine))
    cli.run()


if __name__ == "__main__":
    main()
