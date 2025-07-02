from budget.budget_io import YamlBudgetIO
import pytest
from budget.expense import ExpenseItem, ExpenseType
from budget.budget_month import BudgetMonth
import datetime
import sys

def test_yaml() -> None:
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
    yaml_io = YamlBudgetIO()
    yaml_io.export_budget(budget_month)
    new_budget_month = yaml_io.import_budget(6, 2025)

    assert new_budget_month.month == 6
    assert new_budget_month.year == 2025
    assert len(new_budget_month.expenses) == 3

if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
