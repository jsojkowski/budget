from pathlib import Path
from abc import ABC, abstractmethod
from budget.budget_month import BudgetMonth
from budget.expense import ExpenseItem
from datetime import date
from enum import Enum
from typing import Optional
# class syntax
class IOType(Enum):
    YAML = 1
    XLXS = 2
    LATEX = 3
   
class BudgetIO(ABC):
    def __init__(self, filepath: Path) -> None:
        self.filepath: Path = filepath
        self.extension = None
        self.type: Optional[IOType] = None

    def import_budget(self, month: int, year: int) -> BudgetMonth:
        pass

    @abstractmethod
    def export_budget(self, month: date, budget: list[ExpenseItem]) -> None:
        pass
    
    def get_filepath(self, month: int, year: int) -> None:
        name = f"{year}_{month}_budget.{self.extension}"
        return self.filepath / self.extension / name
