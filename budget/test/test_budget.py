from budget.budget import Budget, DEFAULT_DAY_KEY
import pytest
from budget.expense import ExpenseItem, ExpenseType, ExpenseSource
from budget.budget_month import BudgetMonth
import datetime
import sys

def test_add_expense(tmp_path) -> None:
    test_path = tmp_path / "example.db"
    budget = Budget(test_path)
    june = datetime.date(2025,6,DEFAULT_DAY_KEY)
    test_expense = ExpenseItem(name="rent", 
            amount=1300, 
            description="All shared expenses that come out of bug account.", 
            category=ExpenseType.FIXED,
            date=datetime.date(2025,6, 2),
            source=ExpenseSource.BANK_STATEMENT
            )
    budget.add_expense(test_expense)
    assert budget.num_expenses() == 1
    assert len(budget.get_expenses_by_month(june)) == 1

    test_expense = ExpenseItem(name="gas", 
        amount=35.23, 
        description="Gas.", 
        category=ExpenseType.GAS,
        date=datetime.date(2025,6,10),
        source=ExpenseSource.CC_STATEMENT
        )
    budget.add_expense(test_expense)
    assert budget.num_expenses() == 2
    assert len(budget.get_expenses_by_month(june)) == 2

    test_expense = ExpenseItem(name="rent", 
        amount=1300, 
        description="All shared expenses that come out of bug account.", 
        category=ExpenseType.FIXED,
        date=datetime.date(2025,7,1),
        source=ExpenseSource.BANK_STATEMENT
        )
    budget.add_expense(test_expense)
    july = datetime.date(2025,7,DEFAULT_DAY_KEY)
    assert budget.num_expenses() == 3
    assert len(budget.get_expenses_by_month(july)) == 1


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
