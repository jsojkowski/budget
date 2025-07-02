from common.input_util import get_input_with_condition, get_input_not_empty
from typing import Final, List, Dict
from budget.expense import ExpenseItem, ExpenseType
import datetime
from pathlib import Path
import yaml

BASE_EXPENSE_LIST: Final= [
ExpenseItem(name="rent", 
            price=1300, 
            description="All shared expenses that come out of bug account.", 
            category=ExpenseType.FIXED,
            date=datetime.date(2025,6,1)
            ), 
]

DEFAULT_INCOME = 2000.00

class BudgetMonth:
    def __init__(self, month: int, year: int, income: float = DEFAULT_INCOME) -> None:
        self.expenses: List[ExpenseItem] = []
        self._filtered_expenses_by_category = {}
        self._is_filter_cached = False
        self.income = income
        self.month: datetime.date.month = month
        self.year: int = year

    def combine(self, new_month) -> None:
        if len(new_month.expenses) > 0:
            self.expenses.append(new_month.expenses)
            self._is_filter_cached = False


    def _filter_expenses_by_category(self) -> None:
        """Checks if the expenses have been sorted. If they have not, sort them.
        """
        if self._is_filter_cached:
            return
        temp_dict = {}
        for expense in self.expenses:
            if expense.category in temp_dict.keys():
                temp_dict[expense.category].append(expense)
            else:
                temp_dict[expense.category] = [expense]

        for key, value in temp_dict.items():
            self._filtered_expenses_by_category[key] = sorted(value, key=lambda item: item.date)
        self._is_filter_cached = True

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
        for category, expenses in self._filtered_expenses_by_category.items():
            for expense in expenses:
                category_total += expense.price
            print(f"\t\t{category}: {category_total}")
            total += category_total
            category_total = 0.0
        print(f"\tTotal spent: {total}")

    def add_expense(self, expense_item :ExpenseItem) -> None:
        self.expenses.append((expense_item))
        self._is_filter_cached = False
    
    def add_expenses_yaml(self, filename: Path) -> None:
        with open(filename, 'r') as file:
            data = yaml.safe_load(file)
        for item in data["expenses"]:
            self.expenses.append(ExpenseItem(name = item["name"], price=item["price"], description=item["description"], category=getattr(ExpenseType, item["category"]), date=datetime.fromisoformat(item["date"])))
        self._is_filter_cached = False

    def write_spreadsheet(self, filename: Path) -> None:
        """Write the current month to an excel file

        Args:
            filename (Path): the path to write to
        """
        raise NotImplementedError

    def write_yaml(self, output_path: Path) -> None:
        """Write the current month to an excel file

        Args:
            output_path (Path): the path to write to
        """
        file_path = output_path / f"{self.month}_{self.year}.yaml"
        with open(file_path, "w", encoding = "utf-8") as yaml_file:
            dump = yaml.dump(self.dict, default_flow_style = False, allow_unicode = True, encoding = None)
            yaml_file.write( dump )

    @staticmethod
    def create(cls):
        """Create a Budget Month from user input

        Returns:
            BudgetMonth: _description_
        """
        month = int(input("Enter month: "))
        year = input("Enter year (press `enter` key for current year): ")
        if len(year) == 0:
            current_datetime = datetime.now()
            year = current_datetime.year
        else:
            year = int(year)
        income_str = input("Enter income: ")
        income = float(income_str) if len(income_str) > 0 else DEFAULT_INCOME
        return cls(month=month,
                        year=year,
                        income=income)
