# https://jeltef.github.io/PyLaTeX/current/
# https://jeltef.github.io/PyLaTeX/current/examples/full.html
from budget.budget_io import BudgetIO, IOType
from budget.expense import ExpenseItem
import datetime
from pathlib import Path
from common.consts import DATA_DIR

from pylatex import *

class LatexIO(BudgetIO):
    def __init__(self, filepath: Path = DATA_DIR) -> None:
        super().__init__(filepath)
        self.extension = "latex"
        self.type = IOType.LATEX
        self.doc = None

    def export_budget(self, month: datetime.date, entries: list[ExpenseItem]) -> None:
        geometry_options = {"tmargin": "3cm", "lmargin": "2cm"}
        self.doc = Document(geometry_options=geometry_options)
        self.create_expense_table(entries)
        self.doc.generate_pdf(self.get_filepath(month.month, month.year), clean_tex=True)

    def create_expense_table(self, expenses: list[ExpenseItem]):
        with self.doc.create(Section("Expenses")):
            self.doc.append("All Expenses for this period.")
            with self.doc.create(Subsection("Expense Table")):
                with self.doc.create(LongTable("|| c c c c c p{4cm} ||")) as table:
                    table.add_hline()
                    # table.append(NoEscape(r'\setlength{\tabcolsep}{4pt}'))
                    table.add_hline()
                    table.add_row(Command('thead', "Category"), Command('thead', "Date"), Command('thead', "Name"), Command('thead', "Amount"), Command('thead', "Source"),Command('thead',  "Description"))
                    # table.add_row("Category", "Date", "Name", "Amount", "Source", "Description")
                    table.add_hline()
                    table.add_hline()
                    current_category = None
                    income = 0.0
                    spent = 0.0
                    for expense_item in expenses:
                        category_field = ""
                        if current_category == None:
                            category_field = expense_item.category.name
                        elif current_category != expense_item.category:
                            category_field = expense_item.category.name
                        current_category = expense_item.category
                        table.add_row((category_field, expense_item.date.strftime("%m-%d-%Y"), expense_item.name, expense_item.amount, expense_item.source.name, expense_item.description))
                        table.add_hline()
                    table.add_hline()
                    table.add_row(("TOTAL INCOME", '', '', '', '', income))
                    table.add_row(("TOTAL SPENT", '', '', '', '', spent))
                    table.add_row(("NET TOTAL", '', '', '', '', income - spent))

                    