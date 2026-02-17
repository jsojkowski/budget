from budget.budget_io import YamlBudgetIO, BudgetIO
import pytest
from budget.expense import ExpenseItem, ExpenseType, ExpenseSource
from budget.budget_month import BudgetMonth
import datetime
import sys
from unittest.mock import patch

@patch('budget.budget_io.BudgetIO.get_filepath')
def test_yaml(mock_get_file_path, tmp_path) -> None:
    mock_get_file_path.return_value = tmp_path / "test.yaml"
    budget_month = BudgetMonth(6, 2025)
    fixed_expense = ExpenseItem(name="rent", 
        amount=1300, 
        description="All shared expenses that come out of bug account.", 
        category=ExpenseType.FIXED,
        date=datetime.date(2025,7,1),
        source=ExpenseSource.BANK_STATEMENT
        )
    gas_expense = ExpenseItem(name="gas", 
        amount=35.21, 
        description="All shared expenses that come out of bug account.", 
        category=ExpenseType.GAS,
        date=datetime.date(2025,7,1),
        source=ExpenseSource.CC_STATEMENT
        )
    gas_expense2 = ExpenseItem(name="gas", 
        amount=25.21, 
        description="All shared expenses that come out of bug account.", 
        category=ExpenseType.GAS,
        date=datetime.date(2025,7,12),
        source=ExpenseSource.CC_STATEMENT
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
    assert new_budget_month.expenses[0].amount == 1300
    assert new_budget_month.expenses[0].category == ExpenseType.FIXED
    assert new_budget_month.expenses[0].source == ExpenseSource.BANK_STATEMENT
    assert new_budget_month.expenses[0].date == datetime.date(2025,7,1)

if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
