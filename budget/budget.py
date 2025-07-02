from dataclasses import dataclass
from enum import Enum
from typing import Final, List, Dict
import datetime
from pathlib import Path
import yaml

from common.input_util import get_input_with_condition, get_input_not_empty
from budget.budget_month import BudgetMonth
from budget.expense import ExpenseItem

DEFAULT_DAY_KEY: Final = 1

class Budget:
    """Holds the all budget info."""

    def __init__(self) -> None:
        #: months in the budget
        self.months: Dict[datetime.date, BudgetMonth] = {}


    def add_expense(self, new_expense: ExpenseItem = None) -> None:
        """Add a new expense item to the budget based on the date of the item.

        Args:
            new_expense (ExpenseItem): The item to add, None if you want to create the item in this method
        """
        if new_expense is None:
            new_expense = ExpenseItem.create()
        date_key = datetime.date(new_expense.date.year, new_expense.date.month, DEFAULT_DAY_KEY)
        if date_key in self.months.keys():
            self.months[date_key].add_expense(new_expense)
        else:
            self.months[date_key] = BudgetMonth(new_expense.date.month, new_expense.date.year)
            self.months[date_key].add_expense(new_expense)


    def add_expenses_xlxs(self, filename: Path) -> None:
        raise NotImplementedError

    def create_month(self, new_month: BudgetMonth = None) -> BudgetMonth:
        if new_month is None:
            new_month = BudgetMonth.create()
        date_key = datetime.date(new_month.year, new_month.month, DEFAULT_DAY_KEY)

        # if the new month already exists, combine the months
        if date_key in self.months.keys():
            new_month = new_month.combine(self.months[date_key])
        self.months[date_key] = new_month
        return new_month