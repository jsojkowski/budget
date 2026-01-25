from dataclasses import dataclass
from enum import Enum, auto
from typing import Final, List, Dict, Tuple
import datetime

from common.input_util import get_input_with_condition, get_input_not_empty


# class syntax
class ExpenseType(Enum):
    FIXED = auto()
    GROCERY = auto()
    RESTAURANT  = auto()
    RESTAURANT_WORK_LUNCH = auto()
    CAR_MAINTENANCE = auto()
    GAS = auto()
    PADDINGTON_FOOD = auto()
    PADDINGTON_VET = auto()
    ENTERTAINMENT = auto()
    SHOPPING_CLOTHES = auto()
    SHOPPING_MAKEUP = auto()
    SHOPPING = auto()
    TRAVEL = auto()
    GIFTS = auto()
    CHARITY = auto()
    CC_PAYMENT = auto()
    PAYROLL = auto()
    CHECK = auto()

def is_expense(value):
    return int(value) < 11

def get_expense_type_list():
    members = ""
    for member in ExpenseType:
        members += f"\n{member.value}: {member.name}"
    return members

@dataclass
class ExpenseItem:
    """Class for keeping track of an item in inventory."""
    name: str
    amount: float
    description: str
    category: ExpenseType
    date: datetime.date
    debug_line: str = ""


    def print(self):
        print(f"Name: {self.name}")
        print(f"Amount: {self.amount}")
        print(f"Description: {self.description}")
        print(f"Category: {self.category.name}")
        print(f"Date: {self.date}")
    
    @classmethod
    def create_from_input(cls):
        """Add an expense from user input.

        Returns:
            ExpenseItem: The Expense Item
        """
        name = input("Enter Expense Name: ")
        amount = float(input("Enter amount: "))
        description = input("Enter description: ")
        is_value = lambda x: int(x) in [e.value for e in ExpenseType]
        category = ExpenseType(int(get_input_with_condition(f"{get_expense_type_list()}\nEnter the number for the Category: ",  is_value)))
        date_string = input("Enter date as MM/DD/YYYY: ")
        month, day, year = date_string.split("/")
        date = datetime.date(int(year), int(month), int(day))
        return cls(name=name,
                        amount=amount,
                        description=description,
                        category=category,
                        date=date)
    