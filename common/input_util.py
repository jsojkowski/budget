from typing import Callable, List, Optional, Tuple
from logging import info, warning, error

def is_in_list(item, list) -> bool:
    return item in list

def query_yes_no(question: str, default: bool = True) -> bool:
    """Ask a yes/no question via input() and return their answer.

    :param question: A question that accepts yes or no answers
    :param default: The default action when user does not respond explicitly
    :return: True or False to indicate the user input
    """
    # inputs that are considered as valid
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}

    if default:
        prompt = " [Y/n] "
    # Else default is False
    else:
        prompt = " [y/N] "

    while True:
        choice = input(question + prompt).lower()
        if choice == "":
            return default
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def is_string_empty(string: str) -> bool:
    """Check that the length of the string is zero.

    :param string: the string to check
    :return: True if the string is length 0, false otherwise
    """
    return len(string.strip()) == 0


def is_alphanumeric(string: str) -> bool:
    """Check that a string contains only alphanumeric characters.

    :param string: the string to test
    :return: True if the string is alphanumeric, false otherwise
    """
    regexp = re.compile("[^0-9a-zA-Z]+")
    return regexp.search(string) is None


def get_input_with_condition(string: str, is_valid: Optional[Callable[[str], bool]] = None, error_print: str = "") -> str:
    """Get and validate input from a user.

    :param string: the string to print when prompting the user
    :param is_valid: optional additional lambda function to validate user input,
        defaults to None which is converted to a lambda returning True
    :param error_print: optional warning string to print out if the input is not valid
    :return: The string from the user input
    """
    if is_string_empty(error_print):
        error_print = "Invalid Entry!"
    if is_valid is None:
        # assign is_valid to always be true
        def is_valid(input):
            return True

    input_str = str(input(string).strip())
    while not is_valid(input_str):
        warning(error_print)
        input_str = str(input(string).strip())
    return input_str


def get_input_not_empty(string: str, is_valid: Optional[Callable[[str], bool]] = None, error_print: str = "") -> str:
    """Get and validate input from a user.

    :param string: the string to print when prompting the user
    :param is_valid: optional additional lambda function to validate user input,
        defaults to None which is converted to a lambda returning True
    :param error_print: optional warning string to print out if the input is not valid
    :return: The string from the user input
    """
    if is_string_empty(error_print):
        error_print = "Invalid Entry!"
    if is_valid is None:
        # assign is_valid to always be true
        def is_valid(input):
            return True

    input_str = str(input(string).strip())
    while ((not is_string_empty(input_str)) and (is_valid(input_str))) == False:
        warning(error_print)
        input_str = str(input(string).strip())
    return input_str
