import pymupdf4llm
from datetime import date
from typing import List, Tuple
from pathlib import Path
from budget.expense import ExpenseItem, ExpenseType, get_expense_type_list, is_expense
from budget.expense_type_map import TYPE_MAP
from common.input_util import get_input_with_condition, get_input_not_empty

class CreditCardStatement:

    def __init__(self, path: Path) -> None:
        self.path = path 
        self.expenses = []
        self.interest_charged: float = 0.0
        self.total_credits: float = 0.0
        self.total_expenses: float = 0.0
        self.year = int(path.name.split("_")[1].split("-")[0])
        self.month = int(path.name.split("_")[1].split("-")[1])
        self.parsePdf()

    def parsePdf(self):
        md_read = pymupdf4llm.LlamaMarkdownReader()
        data = md_read.load_data(self.path)

        # TODO: need to get all pages that could have data
        page_two_text = data[2].text_resource.text
        self.parse_pdf_page(page_two_text.split("\n"))
        if "continued on next page..." in page_two_text:
            self.parse_pdf_page(data[3].text_resource.text.split("\n"))

    def parse_pdf_page(self, page_text: list[str]) -> None:
        is_payment_credit = False
        is_purchase = False
        for line in page_text:
            if len(line.strip()) == 0:
                continue
            if "Payments and Other Credits" in line:
                is_payment_credit = True
                is_purchase = False
            elif "Purchases and Adjustments" in line:
                is_payment_credit = False
                is_purchase = True
            elif "Interest Charged" in line:
                is_payment_credit = False
                is_purchase = False
            elif "TOTAL INTEREST CHARGED FOR THIS PERIOD" in line:
                self.interest_charged = float(line.split()[-1].strip("$"))
                # end of statement
                return
            elif "/" in line.split()[0]:
                if is_payment_credit:
                    self.total_credits += self.create_expense_from_line(line).amount
                elif is_purchase:
                    expense = self.create_expense_from_line(line)
                    self.total_expenses += expense.amount
                    self.expenses.append(expense)


    def create_expense_from_line(self, line: str) -> ExpenseType:
        debug_line = line

        line_split = line.split()
        month, day = line_split[0].strip().split("/")

        # Convert the full date string to a datetime object
        expense_date = date(self.year, int(month), int(day))
        description = " ".join(line.split("1714")[0].split()[2::]).strip()
        amount = float(line.split("1714")[1].strip().replace(',', ''))
        name, category = self.parse_expense(description)
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
