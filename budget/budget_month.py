from common.input_util import get_input_with_condition, get_input_not_empty
from typing import Final, List, Dict
from budget.expense import ExpenseItem, ExpenseType
import datetime
from pathlib import Path
import yaml
from calendar import Month

class BudgetMonth:
    def __init__(self, month: int, year: int) -> None:
        self.expenses: List[ExpenseItem] = []
        self.filtered_expenses_by_category = {}
        self.income = 0.0
        self.month: Month = Month(month)
        self.year: int = year

    def combine(self, new_month) -> None:
        self.expenses += new_month.expenses
        self._filter_expenses_by_category()


    def _filter_expenses_by_category(self) -> None:
        """Checks if the expenses have been sorted. If they have not, sort them.
        """
        temp_dict = {}
        for expense in self.expenses:
            if expense.category in temp_dict.keys():
                temp_dict[expense.category].append(expense)
            else:
                temp_dict[expense.category] = [expense]

        for key, value in temp_dict.items():
            self.filtered_expenses_by_category[key] = sorted(value, key=lambda item: item.date)

    def print(self) -> None:
        """Print month info.
        """
        print(f"Current Month: {self.month}-{self.year}")
        print(f"\tIncome: {self.income}")
        print(f"\tNumber of transactions: {len(self.expenses)}")
        print("\tCategory Breakdown:")
        self._filter_expenses_by_category()
        category_total = 0.0
        total = 0.0
        for category, expenses in self.filtered_expenses_by_category.items():
            for expense in expenses:
                category_total += expense.amount
            print(f"\t\t{category}: {category_total}")
            total += category_total
            category_total = 0.0
        print(f"\tTotal spent: {total}")

    def add_expense(self, expense_item: ExpenseItem) -> None:
        if expense_item.name == "Ford Motor Company Payroll":
            self.income += expense_item.amount
        self.expenses.append(expense_item)
        self._filter_expenses_by_category()
    
    def add_expenses_yaml(self, filename: Path) -> None:
        with open(filename, 'r') as file:
            data = yaml.safe_load(file)
        for item in data["expenses"]:
            self.expenses.append(ExpenseItem(name = item["name"], amount=item["amount"], description=item["description"], category=getattr(ExpenseType, item["category"]), date=datetime.fromisoformat(item["date"])))
        self._filter_expenses_by_category()

    def write_spreadsheet(self, filename: Path) -> None:
        """Write the current month to an excel file

        Args:
            filename (Path): the path to write to
        """
        raise NotImplementedError

    def write_yaml(self, output_path: Path) -> None:
        """Write the current month to a yaml

        Args:
            output_path (Path): the path to write to
        """
        file_path = output_path / f"{self.month}_{self.year}.yaml"
        with open(file_path, "w", encoding = "utf-8") as yaml_file:
            dump = yaml.dump(self.dict, default_flow_style = False, allow_unicode = True, encoding = None)
            yaml_file.write( dump )

    @classmethod
    def create(cls):
        """Create a Budget Month from user input

        Returns:
            BudgetMonth: _description_
        """
        month = int(input("Enter month: "))
        year = input("Enter year (press `enter` key for current year): ")
        if len(year) == 0:
            current_datetime = datetime.date.today()
            year = current_datetime.year
        else:
            year = int(year)
        income_str = input("Enter income: ")
        income = float(income_str)
        return cls(month=month,
                        year=year,
                        income=income)
