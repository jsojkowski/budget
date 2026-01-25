from typing import Final, List, Dict
import datetime
from pathlib import Path
import glob
from budget.budget_month import BudgetMonth
from budget.expense import ExpenseItem
from budget.budget_io import IOType, IOFactory
from pdf_reader.credit_card_statement import CreditCardStatement
from pdf_reader.bank_statement import BankStatement
from common.consts import PDF_DATA_DIR

DEFAULT_DAY_KEY: Final = 1

class Budget:
    """Holds the all budget info."""

    def __init__(self) -> None:
        #: months in the budget
        self.months: Dict[datetime.date, BudgetMonth] = {}
        self.io_factory = IOFactory()

    def get_month_key(self,year, month ):
        return datetime.date(year,month, DEFAULT_DAY_KEY)
    

    def add_expense(self, new_expense: ExpenseItem = None) -> None:
        """Add a new expense item to the budget based on the date of the item.

        Args:
            new_expense (ExpenseItem): The item to add, None if you want to create the item in this method
        """
        if new_expense is None:
            new_expense = ExpenseItem.create_from_input()
        date_key = self.get_month_key(new_expense.date.year, new_expense.date.month)
        if date_key in self.months.keys():
            self.months[date_key].add_expense(new_expense)
        else:
            self.months[date_key] = BudgetMonth(new_expense.date.month, new_expense.date.year)
            self.months[date_key].add_expense(new_expense)
    
    def load_all_statements(self) -> None:
        # TODO  - test this out
        for file in glob.glob((PDF_DATA_DIR / "data/pdf/**/checking/*.pdf").as_posix()):
            statement = BankStatement(Path(file))
            for expense in statement.expenses:
                month_key = self.get_month_key(expense.date.year, expense.date.month)
                if month_key not in self.months.keys():
                    self.months[month_key] = BudgetMonth(expense.date.month, expense.date.year)
                self.months[month_key].expenses.append(expense)
        for file in glob.glob((PDF_DATA_DIR / "data/pdf/**/credit_card/*.pdf").as_posix()):
            statement = CreditCardStatement(Path(file))
            for expense in statement.expenses:
                month_key = self.get_month_key(expense.date.year, expense.date.month)
                if month_key not in self.months.keys():
                    self.months[month_key] = BudgetMonth(expense.date.month, expense.date.year)
                self.months[month_key].expenses.append(expense)
        print(self.months)


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
    
    def export(self, format_type: IOType = IOType.YAML) -> None:
        for month, data in self.months.items():
            print(f"Exporting month: {month}")
            self.io_factory.get_io(format_type).export_budget(data)