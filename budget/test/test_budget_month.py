import pytest
from budget.expense import ExpenseItem, ExpenseType
from budget.budget_month import BudgetMonth
import datetime
import sys

def test_add_expense() -> None:
    budget_month = BudgetMonth(6, 2025)
    test_expense = ExpenseItem(name="rent", 
        price=1300, 
        description="All shared expenses that come out of bug account.", 
        category=ExpenseType.FIXED,
        date=datetime.date(2025,7,1)
        )
    budget_month.add_expense(test_expense)
    assert len(budget_month.expenses) == 1
    assert budget_month._is_filter_cached == False

def test_filter_expenses() -> None:
    budget_month = BudgetMonth(6, 2025)
    fixed_expense = ExpenseItem(name="rent", 
        price=1300, 
        description="All shared expenses that come out of bug account.", 
        category=ExpenseType.FIXED,
        date=datetime.date(2025,7,1)
        )
    gas_expense = ExpenseItem(name="gas", 
        price=35.21, 
        description="All shared expenses that come out of bug account.", 
        category=ExpenseType.GAS,
        date=datetime.date(2025,7,1)
        )
    gas_expense2 = ExpenseItem(name="gas", 
        price=25.21, 
        description="All shared expenses that come out of bug account.", 
        category=ExpenseType.GAS,
        date=datetime.date(2025,7,12)
        )
    budget_month.add_expense(fixed_expense)
    budget_month.add_expense(gas_expense)
    budget_month.add_expense(gas_expense2)
    budget_month._filter_expenses_by_category()
    assert len(budget_month._filtered_expenses_by_category.keys()) == 2
    assert ExpenseType.GAS in budget_month._filtered_expenses_by_category.keys()
    assert len(budget_month._filtered_expenses_by_category[ExpenseType.GAS]) == 2
    assert budget_month._is_filter_cached == True
    
    gas_expense3 = ExpenseItem(name="gas", 
        price=38.21, 
        description="All shared expenses that come out of bug account.", 
        category=ExpenseType.GAS,
        date=datetime.date(2025,7,22)
        )
    budget_month.add_expense(gas_expense3)
    assert budget_month._is_filter_cached == False
    previous_date = datetime.date(2000,7,22)
    for item in budget_month._filtered_expenses_by_category[ExpenseType.GAS]:
        assert item.date > previous_date
        previous_date = item.date

def test_combine_months() -> None:
    budget_month1 = BudgetMonth(6, 2025)
    budget_month2 = BudgetMonth(6, 2025)
    fixed_expense = ExpenseItem(name="rent", 
        price=1300, 
        description="All shared expenses that come out of bug account.", 
        category=ExpenseType.FIXED,
        date=datetime.date(2025,7,1)
        )
    gas_expense = ExpenseItem(name="gas", 
        price=35.21, 
        description="All shared expenses that come out of bug account.", 
        category=ExpenseType.GAS,
        date=datetime.date(2025,7,1)
        )
    budget_month1.add_expense(fixed_expense)
    budget_month1.add_expense(gas_expense)
    gas_expense2 = ExpenseItem(name="gas", 
        price=25.21, 
        description="All shared expenses that come out of bug account.", 
        category=ExpenseType.GAS,
        date=datetime.date(2025,7,12)
        )
    budget_month2.add_expense(gas_expense2)

    budget_month1.combine(budget_month2)
    assert len(budget_month1.expenses) == 3




if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
