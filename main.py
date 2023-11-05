#!/usr/bin/env python3
from app import Indexer, CLIApplication, SearchEngine
from app.command import (
    IndexCommand,
    SearchFileDirCommand,
    SearchInfoCommand,
    SearchFileDirInfoCommand,
)


def main():
    indexer = Indexer()
    search_engine = SearchEngine()

    # sys.argv = ["main.py", "index", "."]
    # sys.argv = ["main.py", "info", "xxx", "."]
    # sys.argv = ["main.py", "info", "xxx", "-i", "index.pkl"]
    # sys.argv = ["main.py", "searchfd", "ewmyj", "-i", "index.pkl"]
    # sys.argv = ["main.py", "searchfd", "ewmyj", "."]
    # sys.argv = ["main.py", "searchfdi", "xxx", "..ext", "-i", "index.pkl"]
    # sys.argv = ["main.py", "searchfdi", "xxx", "..ext", "."]

    cli = CLIApplication()
    cli.register_command(IndexCommand(indexer))
    cli.register_command(SearchInfoCommand(search_engine))
    cli.register_command(SearchFileDirCommand(search_engine))
    cli.register_command(SearchFileDirInfoCommand(search_engine))
    cli.run()


if __name__ == "__main__":
    main()
