BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
ORANGE = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
CYAN = '\033[36m'
GREY = '\033[37m'
WHITE = '\033[38m'
RESET = '\033[39m'
DEFAULT_COLOR = "\033[0m"


def print_with_color(msg: any = "", color: str = DEFAULT_COLOR) -> None:
    """
    Prints a message in a given color.
    Parameters: msg (str), color (str)
    Returns: Nothing
    """
    print(color + str(msg) + DEFAULT_COLOR)


def print_error(msg: any = "") -> None:
    """
    Prints an error message in red.
    Parameters: msg (str)
    Returns: Nothing
    """
    print_with_color(msg, RED)


def print_debug(msg: any = "") -> None:
    """
    Prints a debug message in blue.
    Parameters: msg (str)
    Returns: Nothing
    """
    print_with_color(msg, BLUE)
