import sys
from typing import List
import os
# class syntax
from enum import Enum
from common.input_util import get_input_with_condition
from budget.budget import Budget, ExpenseItem 

class MainMenuOptions(Enum):
    CREATE_EXPENSE = 1
    EXPORT_EXPENSES = 2
    VIEW_EXPENSES = 3
    NEW_MONTH = 4
    PRINT_MONTH = 4

def get_main_menu_list():
    members = ""
    for member in MainMenuOptions:
        members += f"\n{member.value}: {member.name}"
    return members

def main(argv: List[str]) -> int:
    """Entrypoint for using budget tool.

    :param argv: List of strings to be parsed by ArgumentParse -- dbc file name.
    :return: Exit code
    """
    help_menu = f"Welcome to Budget Program. Please enter the index for an item below:{get_main_menu_list()}"
    is_value = lambda x: int(x) in [e.value for e in MainMenuOptions]
    selected_option = MainMenuOptions(int(get_input_with_condition(help_menu, is_value)))
    all_months = Budget()
    current_month = all_months.create_month()
    while(True):
        match selected_option:
            case MainMenuOptions.NEW_MONTH:
                current_month = all_months.create_month()
            case MainMenuOptions.CREATE_EXPENSE:
                all_months.add_expense()
            case MainMenuOptions.EXPORT_EXPENSES:
                print("Prepare to stop or go. The light is yellow.")
            case MainMenuOptions.VIEW_EXPENSES:
                print("Go! The light is green.")
            case MainMenuOptions.PRINT_MONTH:
                current_month.print()
            case _:  # Default case for any other value
                print("Unknown menu option.")
                return os.EX_SOFTWARE
        selected_option = MainMenuOptions(int(get_input_with_condition(help_menu, is_value)))


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as e:
        print(f"Caught exception, see traceback below for details:\n {e}")
        sys.exit(1)
