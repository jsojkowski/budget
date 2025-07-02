from dataclasses import dataclass
from enum import Enum
from typing import Final, List, Dict
import datetime

from common.input_util import get_input_with_condition, get_input_not_empty


# class syntax
class ExpenseType(Enum):
    FIXED = 1
    GROCERY = 2
    RESTAURANT  = 3
    RESTAURANT_WORK_LUNCH = 4
    CAR_MAINTENANCE = 5
    GAS = 6
    PADDINGTON_FOOD = 7
    PADDINGTON_VET = 8
    ENTERTAINMENT = 9
    TRAVEL = 10

def get_expense_type_list():
    members = ""
    for member in ExpenseType:
        members += f"\n{member.value}: {member.name}"
    return members

@dataclass
class ExpenseItem:
    """Class for keeping track of an item in inventory."""
    name: str
    price: float
    description: str
    category: ExpenseType
    date: datetime.date

    def print(self):
        print(f"Name: {self.name}")
        print(f"Amount: {self.price}")
        print(f"Description: {self.description}")
        print(f"Category: {self.category.name}")
        print(f"Date: {self.date}")
    
    @staticmethod
    def create(cls):
        """Add an expense from user input.

        Returns:
            ExpenseItem: The Expense Item
        """
        name = input("Enter Expense Name: ")
        price = float(input("Enter amount: "))
        description = input("Enter description: ")
        is_value = lambda x: int(x) in [e.value for e in ExpenseType]
        category = ExpenseType(int(get_input_with_condition(f"{get_expense_type_list()}\nEnter the number for the Category: ",  is_value)))
        date_string = input("Enter date as MM/DD/YYYY: ")
        month, day, year = date_string.split("/")
        date = datetime.date(int(year), int(month), int(day))
        return cls(name=name,
                        price=price,
                        description=description,
                        category=category,
                        date=date)
