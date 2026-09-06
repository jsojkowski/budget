import pytest
from budget.expense import ExpenseItem, ExpenseType, ExpenseSource
import datetime
import sys

def test_create_expense() -> None:
    expense  = ('rent', 1300.0, 'All shared expenses that come out of bug account.', 'FIXED', '2025-07-01', 'BANK_STATEMENT', '')
    new_expense = ExpenseItem.create_from_database_row(expense)
    date = datetime.date(2025, 7, 1)
    assert new_expense.name == "rent"
    assert new_expense.amount == 1300.0
    assert new_expense.description == 'All shared expenses that come out of bug account.'
    assert new_expense.category == ExpenseType.FIXED
    assert new_expense.date == date
    assert new_expense.source == ExpenseSource.BANK_STATEMENT
    assert new_expense.debug_line == ''

if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
