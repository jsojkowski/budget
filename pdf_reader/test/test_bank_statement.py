import pytest
import sys
from pdf_reader.bank_statement import BankStatement
from common.consts import PDF_DATA_DIR

def test_bank_statement() -> None:
    bank_statement = BankStatement(PDF_DATA_DIR / "2025/checking/eStmt_2025-04-10.pdf")
    assert bank_statement.year == 2025
    assert bank_statement.month == 4
    assert bank_statement.total_deposits ==  10436.32
    assert bank_statement.total_withdrawals ==  5622.99
    # assert bank_statement.total_difference ==  0.0
    assert bank_statement.beginning_balance ==  1728.84
    assert bank_statement.ending_balance == 5542.17

    assert len(bank_statement.expenses) == 11
    total_difference = 0.0
    for expense in bank_statement.expenses:
        total_difference += expense.amount
    assert total_difference - bank_statement.total_difference < 0.05


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
