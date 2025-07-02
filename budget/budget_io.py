from pathlib import Path
from abc import ABC, abstractmethod
from budget.budget_month import BudgetMonth
from budget.expense import ExpenseItem, ExpenseType
import yaml
from datetime import date
from enum import Enum

DEFAULT_PATH = Path("/Users/juliesojkowski/repo/budget/data")
class BudgetIO(ABC):
    def __init__(self, filepath: Path) -> None:
        self.filepath: Path = filepath
        self.extension = None

    @abstractmethod
    def import_budget(self, month: int, year: int) -> BudgetMonth:
        pass

    @abstractmethod
    def export_budget(self, budget: BudgetMonth) -> None:
        pass
    
    def get_filepath(self, month: int, year: int) -> None:
        return self.filepath / self.extension /f"{year}_{month}_budget.{self.extension}"

class YamlBudgetIO(BudgetIO):
    def __init__(self, filepath: Path = DEFAULT_PATH) -> None:
        super().__init__(filepath)
        self.extension = "yaml"
    
    def import_budget(self, month: int, year: int) -> BudgetMonth:
        input_filepath = self.get_filepath(month, year) 
        with open(input_filepath, "r") as import_file:
            try:
                budget_yaml = yaml.safe_load(import_file)
                budget = BudgetMonth(month, year)
                budget.income = budget_yaml['income']
                for expense in budget_yaml['expenses']:
                    month, day, year = expense['date'].split("-")
                    budget.add_expense(ExpenseItem(
                        name=expense["name"], 
                        price=float(expense['price']),
                        description=expense['description'], 
                        category=ExpenseType(int(expense['category'])),
                        date = date(int(year), int(month), int(day))
                    ))
                return budget
            except yaml.YAMLError as exc:
                print(exc)
    
    def export_budget(self, budget: BudgetMonth) -> None:
        export_filepath = self.get_filepath(budget.month, budget.year) 
        with open(export_filepath, "w+") as export_file:
            export_file.write(f"month: {budget.month}\n")
            export_file.write(f"year: {budget.year}\n")
            export_file.write(f"income: {budget.income}\n")
            export_file.write("expenses:\n")
            for expense in budget.expenses:
                export_file.write(f"  - category: {expense.category.value}\n")
                export_file.write(f"    date: {expense.date.strftime("%m-%d-%Y")}\n")
                export_file.write(f"    description: {expense.description}\n")
                export_file.write(f"    name: {expense.name}\n")
                export_file.write(f"    price: {expense.price}\n")
            