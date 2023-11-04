from .command.sfd import Command
from .exceptions import InvalidCommandException


commands: dict[str, Command] = {}


def register_command(command: Command):
    commands[command.name] = command


def get_command(name: str) -> Command:
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
