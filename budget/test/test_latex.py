import pytest
from budget.expense import ExpenseItem, ExpenseType, ExpenseSource
from budget.budget_latex import LatexIO
import datetime
import sys

def test_create_expense() -> None:
    expense1 = ExpenseItem(name="rent", 
            amount=1300, 
            description="All shared expenses that come out of bug account.", 
            category=ExpenseType.FIXED,
            date=datetime.date(2025,6, 2),
            source=ExpenseSource.BANK_STATEMENT
            )
    expense2 = ExpenseItem(name="gas", 
        amount=35.23, 
        description="Gas", 
        category=ExpenseType.GAS,
        date=datetime.date(2025,6,10),
        source=ExpenseSource.CC_STATEMENT
        )
    expense3 = ExpenseItem(name="gas", 
        amount=20.03, 
        description="Gas", 
        category=ExpenseType.GAS,
        date=datetime.date(2025,6,5),
        source=ExpenseSource.CC_STATEMENT
        )
    
    expense4 = ExpenseItem(name="gas", 
        amount=50.03, 
        description="Gas", 
        category=ExpenseType.GAS,
        date=datetime.date(2025,6,15),
        source=ExpenseSource.CC_STATEMENT
        )
    
    expense5 = ExpenseItem(name="Kroger", 
        amount=150.03, 
        description="Kroger", 
        category=ExpenseType.GROCERY,
        date=datetime.date(2025,6,25),
        source=ExpenseSource.CC_STATEMENT
        )

    latex_gen = LatexIO()
    latex_gen.export_budget(6, 2025, [expense1, expense2, expense3, expense4, expense5])
    

if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
