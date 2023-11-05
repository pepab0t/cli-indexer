from .exceptions import InvalidCommandException

from .interfaces import Executable


class Context:
    commands: dict[str, Executable] = {}
    colors: bool = True


def turn_off_colors():
    Context.colors = False


OPTIONS = {"--no-colors": turn_off_colors}


def register_command(command: Executable):
    Context.commands[command.name] = command


def get_command(name: str) -> Executable:
    """Retrieve registered command.

    Args:
        name (str): Command nam

    Raises:
        InvalidCommandException: raised if comand not found

    Returns:
        Command
    """
    try:
        return Context.commands[name]
    except KeyError:
        raise InvalidCommandException(f"no such command `{name}`")


def apply_options(options: list[str]):
    for opt in options:
        if opt in OPTIONS:
            OPTIONS[opt]()
