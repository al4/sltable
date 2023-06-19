from enum import Enum


class Colour(str, Enum):
    """ An enum of ANSI escape sequences, for colourising text on the console.
    """
    RED = "\x1b[31;20m"
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    PURPLE = "\x1b[35;20m"
    CYAN = "\x1b[36;20m"
    WHITE = "\x1b[37;20m"
    GREY = "\x1b[38;20m"

    BOLD_RED = "\x1b[31;1m"
    BOLD_GREEN = "\x1b[32;1m"
    BOLD_YELLOW = "\x1b[33;1m"
    BOLD_PURPLE = "\x1b[35;1m"
    BOLD_CYAN = "\x1b[36;1m"
    BOLD_WHITE = "\x1b[37;1m"
    BOLD_GREY = "\x1b[38;1m"

    DIM_WHITE = "\x1b[2;20m"

    BOLD = "\x1b[1m"
    RESET = "\x1b[0m"

    def __call__(self, s: object) -> str:
        return f"{self.value}{s!s}{Colour.RESET.value}"

    def __str__(self) -> str:
        return str.__str__(self)

    def print(self, *args, **kwargs):
        """ Print, with a Colour, while preserving other behaviour of the default print function """
        _args = list(args[:])
        # prepend the colour to the first arg
        _args[0] = f"{self.value}{_args[0]}"
        # append reset to the last arg, which may of course also be the first
        _args[-1] = f"{_args[-1]}{Colour.RESET.value}"

        print(*_args, **kwargs)

    def input(self, message: str):
        return input(f"{self.value}{message}{Colour.RESET.value}")
