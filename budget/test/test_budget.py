from budget.budget import Budget, DEFAULT_DAY_KEY
import pytest
from budget.expense import ExpenseItem, ExpenseType
from budget.budget_month import BudgetMonth
import datetime
import sys

def test_add_expense() -> None:
    budget = Budget()
    june = datetime.date(2025,6,DEFAULT_DAY_KEY)
    test_expense = ExpenseItem(name="rent", 
            price=1300, 
            description="All shared expenses that come out of bug account.", 
            category=ExpenseType.FIXED,
            date=datetime.date(2025,6, 2)
            )
    budget.add_expense(test_expense)
    assert len(budget.months) == 1
    assert len(budget.months[june].expenses) == 1

    test_expense = ExpenseItem(name="gas", 
        price=35.23, 
        description="Gas.", 
        category=ExpenseType.GAS,
        date=datetime.date(2025,6,2)
        )
    budget.add_expense(test_expense)
    assert len(budget.months) == 1
    assert len(budget.months[june].expenses) == 2

    test_expense = ExpenseItem(name="rent", 
        price=1300, 
        description="All shared expenses that come out of bug account.", 
        category=ExpenseType.FIXED,
        date=datetime.date(2025,7,1)
        )
    budget.add_expense(test_expense)
    assert len(budget.months) == 2
    july = datetime.date(2025,7,DEFAULT_DAY_KEY)
    assert len(budget.months[july].expenses) == 1

def test_add_expense_create(monkeypatch) -> None:
    budget = Budget()
    test_expense = ExpenseItem(name="rent", 
        price=1300, 
        description="All shared expenses that come out of bug account.", 
        category=ExpenseType.FIXED,
        date=datetime.date(2025,7,1)
        )
    monkeypatch.setattr(ExpenseItem, 'create', lambda _ : test_expense)
    budget.add_expense(test_expense)
    assert len(budget.months) == 1
    july = datetime.date(2025,7,DEFAULT_DAY_KEY)
    assert len(budget.months[july].expenses) == 1


def test_create_month() -> None:
    budget = Budget()
    new_month = BudgetMonth(6,2025)
    assert len(budget.months) == 0
    budget.create_month(new_month)
    assert len(budget.months) == 1
    budget.create_month(new_month)
    assert len(budget.months) == 1
    new_month = BudgetMonth(7,2025)
    budget.create_month(new_month)
    assert len(budget.months) == 2

def create_month():
    return BudgetMonth(7,2025)

def test_add_expense_create(monkeypatch) -> None:
    budget = Budget()
    monkeypatch.setattr(BudgetMonth, 'create', create_month)
    budget.create_month()
    assert len(budget.months) == 1
   

if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
