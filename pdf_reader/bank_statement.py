import pymupdf4llm
from datetime import date
from typing import List, Tuple
from pathlib import Path
from budget.expense import ExpenseItem, ExpenseType, get_expense_type_list, is_expense
from budget.expense_type_map import TYPE_MAP
from common.input_util import get_input_with_condition, get_input_not_empty

class BankStatement:

    def __init__(self, path: Path) -> None:
        self.path = path 
        self.expenses = []
        self.total_difference: float = 0.0
        self.total_deposits: float = 0.0
        self.total_withdrawals: float = 0.0
        self.beginning_balance: float = 0.0
        self.ending_balance: float = 0.0
        self.year = int(path.name.split("_")[1].split("-")[0])
        self.month = int(path.name.split("_")[1].split("-")[1])
        self.parsePdf()

    def parsePdf(self):
        md_read = pymupdf4llm.LlamaMarkdownReader()
        data = md_read.load_data(self.path)

        # TODO: need to get all pages that could have data
        deposits_text = data[2].text_resource.text
        self.deposits_page(deposits_text.split("\n"))
        contd = data[3].text_resource.text
        self.parse_contd_page(contd.split("\n"))

    def parse_contd_page(self, page_text: list[str]) -> None:
        is_withdrawal = False
        is_checks = False
        for line in page_text:
            if len(line.strip()) == 0:
                continue
            if "Withdrawals and other subtractions" in line:
                is_withdrawal = True
            elif "Total withdrawals and other subtractions" in line:
                is_withdrawal = False
                self.total_withdrawals = float(line.split('$')[1].replace(",", '').replace('*', ''))
            elif line.strip() == "Checks":
                is_checks = True
            elif "Total checks" in line:
                # end of statement
                return
            elif "/" in line.split()[0] and is_withdrawal:
                expense = self.create_expense_from_line(line)
                self.total_difference += expense.amount
                self.expenses.append(expense)
            elif "/" in line.split()[0] and is_checks:
                expense = self.create_expense_from_line(line, category=ExpenseType.CHECK)
                self.expenses.append(expense)
                self.total_difference += expense.amount


    def deposits_page(self, page_text: list[str]) -> None:
        is_deposit = False
        for line in page_text:
            if len(line.strip()) == 0:
                continue
            if "Beginning balance on" in line:
                self.beginning_balance: float = float(line.split('$')[1].strip().replace(',', ''))
            elif "Ending balance on" in line:
                self.ending_balance: float = float(line.split('$')[1].strip().replace(',', '').replace('*', ''))
            elif "Deposits and other additions" in line:
                is_deposit = True
            elif "Total deposits and other additions" in line:
                self.total_deposits = float(line.split('$')[1].replace(",", '').replace('*', ''))
                # end of statement
                return
            elif "/" in line.split()[0] and is_deposit:
                expense = self.create_expense_from_line(line)
                self.total_difference += expense.amount
                self.expenses.append(expense)

    def create_expense_from_line(self, line: str, category: ExpenseType = None) -> ExpenseType:
        debug_line = line

        line_split = line.split()
        month, day, year = line_split[0].strip().split("/")

        # Convert the full date string to a datetime object
        expense_date = date(int(year), int(month), int(day))
        description = " ".join(line.split()[1:-1]).strip()
        amount = float(line.split()[-1].strip().replace(',', ''))
        if category is None:
            name, category = self.parse_expense(description)
        else:
            name =  "Check"
        return ExpenseItem(name=name, date=expense_date,description=description, amount=amount, category=category, debug_line=debug_line)
    
    def get_substring(self, description: str) -> str:
        for substring in TYPE_MAP.keys():
            if substring in description:
                return substring
        if "\t" in description:
            return description.split("\t")[0]
        elif "*" in description:
            return description.split("*")[0]
        elif "#" in description:
            return description.split("#")[0]
        return description


    def parse_expense(self, description) -> Tuple[str, ExpenseType]:
        substring = self.get_substring(description)
        if substring in TYPE_MAP.keys():
            return TYPE_MAP[substring]
        category = ExpenseType(int(get_input_with_condition(f"{get_expense_type_list()}\nLINE: {description}\nEnter the number for the Category: ",  is_expense)))
        name = get_input_not_empty("Enter desired name: ")

        TYPE_MAP[substring] = (name, category)
        return TYPE_MAP[substring]

        
# import traceback
# try:
#     print(CreditCardStatement(PROJECT_ROOT_DIR / "data/pdf/eStmt_2025-02-16.pdf"))
# except Exception as e:
#     traceback.print_exc()
#     print(e)
#     print(TYPE_MAP)
