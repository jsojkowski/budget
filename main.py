import sys
from typing import List
import os
# class syntax
from enum import Enum, auto
from common.input_util import get_input_with_condition, get_input_not_empty
from budget.budget import Budget, ExpenseItem 
from pathlib import Path
class MainMenuOptions(Enum):
    LOAD_STATEMENT = auto()
    CREATE_EXPENSE = auto()
    EXPORT_EXPENSES = auto()
    VIEW_EXPENSES = auto()
    NEW_MONTH = auto()
    PRINT_MONTH = auto()

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
    help_menu = f"Welcome to Budget Program. {get_main_menu_list()}\nPlease enter the index for an item above:"
    is_value = lambda x: int(x) in [e.value for e in MainMenuOptions]
    all_months = Budget()

    current_month = None
    all_months.load_statement(Path("/Users/juliesojkowski/repo/budget/data/pdf/eStmt_2025-02-16.pdf"))
    all_months.export()
    return os.EX_SOFTWARE
    # selected_option = MainMenuOptions(int(get_input_with_condition(help_menu, is_value)))
    while(True):
        match selected_option:
            case MainMenuOptions.NEW_MONTH:
                current_month = all_months.create_month()
            case MainMenuOptions.LOAD_STATEMENT:
                path = get_input_not_empty("Enter statement path: ")
                all_months.load_statement(Path(path.strip()))
            case MainMenuOptions.CREATE_EXPENSE:
                all_months.add_expense()
            case MainMenuOptions.EXPORT_EXPENSES:
                all_months.export()
            case MainMenuOptions.VIEW_EXPENSES:
                print("Go! The light is green.")
            case MainMenuOptions.PRINT_MONTH:
                current_month.print()
            case _:
                all_months.export()
                print("Unknown menu option. Saving content and exiting.")
                return os.EX_SOFTWARE
        selected_option = MainMenuOptions(int(get_input_with_condition(help_menu, is_value)))

import traceback

if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as e:
        traceback.print_exc()
        print(f"Caught exception, see traceback below for details:\n {e}")
        sys.exit(1)
