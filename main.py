from app import Indexer, CLIApplication
from app.command import IndexCommand, SearchFileDirCommand, SearchInfoCommand
import sys


def main():
    indexer = Indexer()

    # sys.argv = ["main.py", "index", "."]
    sys.argv = ["main.py", "sinf", "imp", "-i", "index.pkl"]

    cli = CLIApplication()
    cli.register_command(IndexCommand(indexer))
    cli.register_command(SearchInfoCommand(indexer))
    cli.register_command(SearchFileDirCommand(indexer))
    cli.run()


if __name__ == "__main__":
    main()
