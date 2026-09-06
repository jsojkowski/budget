from typing import Final, List, Dict
import datetime
from pathlib import Path
import glob
from budget.budget_month import BudgetMonth
from budget.expense import ExpenseItem, ExpenseType, ExpenseSource
from budget.budget_io import IOType
from budget.io_factory import IOFactory
from pdf_reader.credit_card_statement import CreditCardStatement
from pdf_reader.bank_statement import BankStatement
from common.consts import PDF_DATA_DIR, DATABASE_PATH, EXPENSES_TABLE
from budget.visualization.pie_chart import pie_chart
from calendar import Month
import sqlite3
DEFAULT_DAY_KEY: Final = 1

class Budget:
    """Holds the all budget info."""

    def __init__(self, database_path: Path = DATABASE_PATH) -> None:
        # https://docs.python.org/3/library/sqlite3.html
        self.connection = sqlite3.connect(database_path)
        self.verify_database()
        self.io_factory = IOFactory()

    def  __del__(self):
        self.connection.close()

    def get_month_key(self, year, month):
        return f'{year}-{month}-01'
    
    def verify_database(self):
        if not self.table_exists(EXPENSES_TABLE):
            self.create_expense_table()
    
    def create_expense_table(self):
        cursor = self.connection.cursor()
        cursor.execute(f"CREATE TABLE {EXPENSES_TABLE}(name TEXT NOT NULL, amount REAL NOT NULL, description TEXT NOT NULL, category TEXT NOT NULL, date TEXT NOT NULL, source TEXT NOT NULL, debug_line TEXT NOT NULL) STRICT")

    def table_exists(self, table_name):
        """Checks if a table exists in the SQLite database."""
        cursor = self.connection.cursor()
        # The sqlite_master table stores definitions of all tables
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
        cursor.execute(query, (table_name,))
        result = cursor.fetchone()
        cursor.close()
        # If a row is returned, the table exists
        return result is not None

    def add_expense(self, new_expense: ExpenseItem = None) -> None:
        """Add a new expense item to the budget based on the date of the item.

        Args:
            new_expense (ExpenseItem): The item to add, None if you want to create the item in this method
        """
        if new_expense is None:
            new_expense = ExpenseItem.create_from_input()
        cursor = self.connection.cursor()
        query = f"SELECT name FROM {EXPENSES_TABLE} WHERE name = ? AND amount = ? AND date = ?"
        # Parameters must be passed in a tuple matching the order of the '?'
        params = (new_expense.name, new_expense.amount, new_expense.date.strftime("%Y-%m-%d"))

        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            cursor.execute(f"""
                INSERT INTO {EXPENSES_TABLE} (name, amount, description, category, date, source, debug_line)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (new_expense.name, new_expense.amount, new_expense.description, new_expense.category.name, new_expense.date.strftime("%Y-%m-%d"), new_expense.source.name, new_expense.debug_line))
            self.connection.commit()

    def load_all_statements(self) -> None:
        for file in glob.glob((PDF_DATA_DIR / "**/checking/*.pdf").as_posix()):
            statement = BankStatement(Path(file))
            for expense in statement.expenses:
                self.add_expense(expense)
        for file in glob.glob((PDF_DATA_DIR / "**/credit_card/*.pdf").as_posix()):
            statement = CreditCardStatement(Path(file))
            for expense in statement.expenses:
                self.add_expense(expense)


    def add_expenses_xlxs(self, filename: Path) -> None:
        raise NotImplementedError

    def summary(self, month: str) -> str:
        data = self.get_expenses_by_month(month)
        income = 0.0
        spent = 0.0
        savings = 0.0
        cc_payment = 0.0
        for expense_item in data:
            if expense_item.category == ExpenseType.SAVINGS:
                savings += abs(expense_item.amount)
                continue
            if expense_item.category == ExpenseType.CC_PAYMENT:
                cc_payment += abs(expense_item.amount)
                continue
            match expense_item.source:
                case ExpenseSource.BANK_STATEMENT:
                    if expense_item.amount > 0.0:
                        income += expense_item.amount
                    else:
                        spent += expense_item.amount
                case ExpenseSource.CC_STATEMENT:
                    if expense_item.amount > 0.0:
                        spent += expense_item.amount
                    else:
                        income += expense_item.amount
                case _:
                    continue

        summary = f"TOTAL INCOME: {income} \n"
        summary += f"TOTAL SPENT: {spent} \n"
        summary += f"NET TOTAL: {income - spent} \n"
        summary += f"SAVINGS: {savings} \n"
        summary += f"CC PAYMENT: {cc_payment} \n"
        return summary



    def export(self, month: datetime.date, format_type: IOType = IOType.YAML) -> None:
        print(f"Exporting month: {month}")
        data = self.get_expenses_by_month(month)
        self.io_factory.get_io(format_type).export_budget(month, data)

    def num_expenses(self) -> int:
        cursor = self.connection.cursor()
        res = cursor.execute(f"""
            SELECT COUNT(*) FROM {EXPENSES_TABLE}
        """)
        return res.fetchall()[0][0]

    def get_expenses_by_month_sql(self, month: str, sort_by="ASC", db_column="Date") -> list[ExpenseItem]:
        cursor = self.connection.cursor()
        res = cursor.execute(f"""
            SELECT * FROM {EXPENSES_TABLE}
            WHERE STRFTIME('%Y-%m', date) = ?
            ORDER BY {db_column} {sort_by}
        """, (month,))
        return res.fetchall()

    def get_expenses_by_month(self, month: str) -> list[ExpenseItem]:
        result = self.get_expenses_by_month_sql(month)
        return [ExpenseItem.create_from_database_row(item) for item in result]
    
    def get_distinct_months(self) -> list[str]:
        cursor = self.connection.cursor()
        res = cursor.execute(f"""
            SELECT DISTINCT strftime('%Y-%m', Date) AS year_month FROM {EXPENSES_TABLE} WHERE Date IS NOT NULL ORDER BY year_month DESC
        """,)
        return [str(item).split("'")[1] for item in res.fetchall()]


    # def filter_by_type(self, expense_type: ExpenseType, year: int = 2025, month: Month = None) -> list[ExpenseItem]:
    #     if month:
    #         key = self.get_month_key(year, month.value)
    #         return self.months[key].filtered_expenses_by_category[expense_type]
    #     expenses  = []
    #     for month in self.months.values():
    #         expenses +=  month.filtered_expenses_by_category[expense_type]
    #     return expenses
    

    # def pie_chart(self, expense_types: list[ExpenseType] = [], year: int = 2025, month: Month = None) -> None:
    #         if len(expense_types) == 1:
    #             title = f"Expenses for categories {expense_types[0]} for date: {month.name}/{year}"
    #             expenses  = self.filter_by_type(expense_types[0], year, month)
    #             names = [expense.name for expense in expenses]
    #             amounts = [expense.amount for expense in expenses]  
    #             pie_chart(names, amounts, title)
    #             return
    #         title = f"Expenses with category {", ".join([expense.name for expense in expense_types])} in time {month}/{year}"
    #         if len(expense_types) == 0:
    #             expense_types = [expense_type for expense_type in ExpenseType]
    #             title = f"Expenses in time {month}/{year}"
    #         for expense_type in expense_types:
    #             expenses = self.filter_by_type(expense_type, year, month)
    #             amounts += [expense.amount for expense in expenses]
    #             pie_chart(expense_types, amounts, title)
    #             return

