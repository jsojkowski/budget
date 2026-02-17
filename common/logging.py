

class Colors:
    """Color and style definitions."""

    WHITE = "\033[0;39m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    MAGENTA = "\033[0;35m"
    CYAN = "\033[0;36m"
    STYLE_RESET = "\033[0;0m"
    BOLD = "\033[1m"


TAB = "  "
DEFAULT_DELIMITER_CHARACTER = "="
DEFAULT_DELIMITER_REPEAT_COUNT = 60
DEFAULT_DELIMITER_COLOR = Colors.WHITE

def debug(message) -> None:
    """Prints info message, info header in blue followed by message.

    :param message: message to print
    """
    print_color_msg_with_label(Colors.WHITE, "DEBUG", message)


def info(message) -> None:
    """Prints info message, info header in blue followed by message.

    :param message: message to print
    """
    print_color_msg_with_label(Colors.BLUE, "INFO", message)


def warning(message) -> None:
    """Prints warning message, warning header in yellow followed by message.

    :param message: message to print
    """
    print_color_msg_with_label(Colors.YELLOW, "WARNING", message)


def error(message) -> None:
    """Prints error message, error header in red followed by message.

    :param message: message to print
    """
    print_color_msg_with_label(Colors.RED, "ERROR", message)


def ok(message) -> None:
    """Prints ok message, ok header in green followed by message.

    :param message: message to print
    """
    print_color_msg_with_label(Colors.GREEN, "OK", message)


def print_color_msg_with_label(color, label, message) -> None:
    """Prints message in color with a starting label surrounded in square brackets.

    :param color: color used to print message
    :param label: label to start the message, surrounded in white square brackets
    :param message: message to print
    """
    print(f"{Colors.STYLE_RESET}[{color}{label}{Colors.STYLE_RESET}]{TAB}{color}{message}{Colors.STYLE_RESET}")


def print_color_msg(color, message) -> None:
    """Prints message in color.

    :param color: color used to print message
    :param message: message to print
    """
    print(f"{color}{message}{Colors.STYLE_RESET}")


def print_delimiter(
    character=DEFAULT_DELIMITER_CHARACTER, repeat_count=DEFAULT_DELIMITER_REPEAT_COUNT, color=DEFAULT_DELIMITER_COLOR
) -> None:
    """Prints delimiter string.

    :param character: character to print; default: DEFAULT_DELIMITER_CHARACTER
    :param repeat_count: number of characters to print; default: DEFAULT_DELIMITER_REPEAT_COUNT
    :param color: color of text; default: DEFAULT_DELIMITER_COLOR
    """
    character_string = character * repeat_count
    print_color_msg(color, character_string)


def success_banner(message) -> None:
    """Prints success banner message of passed string.

    :param message: message to print
    """
    print_delimiter(color=Colors.GREEN)
    print_delimiter(color=Colors.GREEN)
    ok(message)
    print_delimiter(color=Colors.GREEN)
    print_delimiter(color=Colors.GREEN)


def warning_banner(message) -> None:
    """Prints warning banner message of passed string.

    :param message: message to print
    """
    print_delimiter(color=Colors.YELLOW)
    print_delimiter(color=Colors.YELLOW)
    warning(message)
    print_delimiter(color=Colors.YELLOW)
    print_delimiter(color=Colors.YELLOW)


def fail_banner(message) -> None:
    """Prints fail banner message of passed string.

    :param message: message to print
    """
    print_delimiter(color=Colors.RED)
    print_delimiter(color=Colors.RED)
    error(message)
    print_delimiter(color=Colors.RED)
    print_delimiter(color=Colors.RED)


def info_banner(message: str, label: str = "INFO", color: Colors = Colors.BLUE) -> None:
    """Prints a noticeable banner in the output terminal with a custom message in a custom color.

    For example, banner would look something like (in color of choice):
    =========================
    =========================
    [label] message
    =========================
    =========================

    :param message: Text to be printed in the middle of the banner
    :param label: Text that precedes `message` in the same line, e.g. "INFO"
    :param color: Text color
    """
    print_delimiter(color=color)
    print_delimiter(color=color)
    print_color_msg_with_label(color=color, label=label, message=message)
    print_delimiter(color=color)
    print_delimiter(color=color)
