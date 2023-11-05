from . import context
from .exceptions import (
    MissingCommandException,
    InvalidCommandException,
    CLIIndexerException,
)
import sys
from .measure import measure_time
from .command import AbstractCommand


def parse_input() -> tuple[list[str], str, list[str]]:
    if len(sys.argv) == 1:
        raise MissingCommandException("no command specified")

    options = []
    i = 1
    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            options.append(arg)
            i += 1
        else:
            break

    try:
        command = sys.argv[i]
    except IndexError:
        raise MissingCommandException("no command specified")

    args = []
    if len(sys.argv) > i:
        args.extend(sys.argv[i + 1 :])

    return options, command, args


class HelpCommand(AbstractCommand):
    name: str = "help"
    doc: str = f"""Find files, dirs or file content in specified directory.
[OPTIONS...] COMMAND ARGUMENTS...
OPTIONS:
    --no-colors     turn off colors

COMMANDS:"""

    def execute(self, args: list[str] = list()) -> None:
        print(
            "\n".join(map(lambda c: c.doc.strip(), context.Context.commands.values()))
        )


class CLIApplication:
    def __init__(self):
        self.register_command(HelpCommand())

    @staticmethod
    def register_command(command: AbstractCommand):
        context.register_command(command)

    @staticmethod
    def print_help():
        try:
            help_c = context.get_command(HelpCommand.name)
        except InvalidCommandException as e:
            print(e)
        else:
            print(help_c.execute())

    @measure_time(lambda res: res == 0)
    def run(self) -> int:
        try:
            options, command, args = parse_input()
        except MissingCommandException as e:
            print(str(e) + "\n")
            self.print_help()
            return 1

        context.apply_options(options)

        try:
            cmd_object = context.get_command(command)
        except InvalidCommandException as e:
            print(str(e) + "\n")
            self.print_help()
            return 1

        try:
            cmd_object.execute(args)
        except CLIIndexerException as e:
            print(str(e) + "\n")
            print(cmd_object.doc.strip())
            return 1

        return 0
