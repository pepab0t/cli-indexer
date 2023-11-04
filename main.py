#!/usr/bin/env python3
from app import Indexer, CLIApplication
from app.command import IndexCommand, SearchFileDirCommand, SearchInfoCommand
import sys


def main():
    indexer = Indexer()

    # sys.argv = ["main.py", "index", "."]
    sys.argv = ["main.py", "sinf", "xxx", "file_struct"]

    cli = CLIApplication()
    cli.register_command(IndexCommand(indexer))
    cli.register_command(SearchInfoCommand(indexer))
    cli.register_command(SearchFileDirCommand(indexer))
    cli.run()


if __name__ == "__main__":
    main()
