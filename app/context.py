from .command import AbstractCommand
from .exceptions import InvalidCommandException


commands: dict[str, AbstractCommand] = {}


def register_command(command: AbstractCommand):
    commands[command.name] = command


def get_command(name: str) -> AbstractCommand:
    """Retrieve registered command.

    Args:
        name (str): Command nam

    Raises:
        InvalidCommandException: raised if comand not found

    Returns:
        Command
    """
    try:
        return commands[name]
    except KeyError:
        raise InvalidCommandException(f"no such command `{name}`")
