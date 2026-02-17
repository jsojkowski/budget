import pytest
import sys
from pdf_reader.credit_card_statement import CreditCardStatement
from common.consts import PDF_DATA_DIR

def test_credit_card_statement() -> None:
    cc_statement = CreditCardStatement(PDF_DATA_DIR / "2025/credit_card/eStmt_2025-05-16.pdf")
    assert cc_statement.year == 2025
    assert cc_statement.interest_charged ==  0.0
    assert cc_statement.total_credits ==  -4161.9
    assert cc_statement.total_expenses - 3372.62 < 0.05
    assert len(cc_statement.expenses) == 57
    total_expenses = 0.0
    for expense in cc_statement.expenses:
        total_expenses += expense.amount
    assert total_expenses - cc_statement.total_expenses < 0.05


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
