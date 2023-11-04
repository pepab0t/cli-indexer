from . import context
from .command import Command, AbstractCommand
from .exceptions import (
    MissingCommandException,
    InvalidCommandException,
    IndexerException,
)
import sys


def parse_input() -> tuple[str, list[str]]:
    if len(sys.argv) == 1:
        raise MissingCommandException("no command specified")

    command = sys.argv[1]
    args = []
    if len(sys.argv) >= 2:
        args.extend(sys.argv[2:])

    return command, args


class HelpCommand(Command):
    name: str = "help"
    doc: str = """Find files, dirs or file content in specified directory.
COMMAND ARGUMENT [OPTIONS ...]"""

    def execute(self, args: list[str] = list()) -> str:
        return "\n".join(map(lambda c: c.doc.strip(), context.commands.values()))


class CLIApplication:
    def __init__(self):
        self.register_command(HelpCommand())

    @staticmethod
    def register_command(command: Command):
        context.register_command(command)

    @staticmethod
    def print_help():
        try:
            help_c = context.get_command(HelpCommand.name)
        except InvalidCommandException as e:
            print(e)
        else:
            print(help_c.execute())

    def run(self):
        try:
            command, args = parse_input()
        except MissingCommandException as e:
            print(str(e) + "\n")
            self.print_help()
            return

        try:
            cmd_object: AbstractCommand = context.get_command(command)
        except InvalidCommandException as e:
            print(str(e) + "\n")
            self.print_help()
            return

        try:
            cmd_object.execute(args)
        except IndexerException as e:
            print(str(e) + "\n")
            print(cmd_object.doc.strip())
