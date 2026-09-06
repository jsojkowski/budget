from pathlib import Path
from budget.budget_month import BudgetMonth
from budget.expense import ExpenseItem, ExpenseType, ExpenseSource
import yaml
from datetime import date
from common.consts import DATA_DIR
from budget.budget_io import BudgetIO, IOType

class YamlIO(BudgetIO):
    def __init__(self, filepath: Path = DATA_DIR) -> None:
        super().__init__(filepath)
        self.extension = "yaml"
        self.type = IOType.YAML
    
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
                        amount=float(expense['amount']),
                        description=expense['description'], 
                        category=ExpenseType[expense['category']],
                        source=ExpenseSource[expense['source']],
                        date = date(int(year), int(month), int(day))
                    ))
                return budget
            except yaml.YAMLError as exc:
                print(exc)
    
    def export_budget(self, month: date, budget: list[ExpenseItem]) -> None:
        export_filepath = self.get_filepath(month.month, month.year) 
        with open(export_filepath, "w+") as export_file:
            export_file.write(f"month: {budget.month}\n")
            export_file.write(f"year: {budget.year}\n")
            export_file.write(f"income: {budget.income}\n")
            export_file.write("expenses:\n")
            for expense in budget.expenses:
                export_file.write(f"  - category: {expense.category.name}\n")
                export_file.write(f"    date: {expense.date.strftime("%m-%d-%Y")}\n")
                export_file.write(f"    description: {expense.description}\n")
                export_file.write(f"    name: {expense.name}\n")
                export_file.write(f"    amount: {expense.amount}\n")
                export_file.write(f"    source: {expense.source.name}\n")
            