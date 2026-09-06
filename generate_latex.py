import sys
from typing import List
from budget.budget import Budget, IOType 
import datetime
import glob
from common.consts import PDF_DATA_DIR
from pdf_reader.credit_card_statement import CreditCardStatement
from pdf_reader.bank_statement import BankStatement
from pathlib import Path

def main(argv: List[str]) -> int:
    """Entrypoint for using budget tool.

    :param argv: List of strings to be parsed by ArgumentParse -- dbc file name.
    :return: Exit code
    """
    budget = Budget()
    statement = CreditCardStatement(PDF_DATA_DIR / "2025/credit_card/eStmt_2025-07-16.pdf")
    for expense in statement.expenses:
        budget.add_expense(expense)
    statement = CreditCardStatement(PDF_DATA_DIR / "2025/credit_card/eStmt_2025-08-16.pdf")
    for expense in statement.expenses:
        budget.add_expense(expense)
    statement = BankStatement(PDF_DATA_DIR / "2025/checking/eStmt_2025-07-11.pdf")
    for expense in statement.expenses:
        budget.add_expense(expense)
    statement = BankStatement(PDF_DATA_DIR / "2025/checking/eStmt_2025-08-11.pdf")
    for expense in statement.expenses:
        budget.add_expense(expense)
    july = datetime.date(2025,7,1)
    budget.export(july, IOType.LATEX)

    
import traceback

if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as e:
        traceback.print_exc()
        print(f"Caught exception, see traceback below for details:\n {e}")
        sys.exit(1)
