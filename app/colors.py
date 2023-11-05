from .context import Context


class Bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def red_text(text: str):
    if Context.colors:
        return f"{Bcolors.FAIL}{text}{Bcolors.ENDC}"
    else:
        return text


def blue_text(text: str):
    if Context.colors:
        return f"{Bcolors.OKBLUE}{text}{Bcolors.ENDC}"
    else:
        return text


def green_text(text: str):
    if Context.colors:
        return f"{Bcolors.OKGREEN}{text}{Bcolors.ENDC}"
    else:
        return text
