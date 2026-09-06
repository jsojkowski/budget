import sys
from typing import List
from budget.budget import Budget, IOType 
import datetime
import glob
from common.consts import PDF_DATA_DIR
from pdf_reader.credit_card_statement import CreditCardStatement
from pdf_reader.bank_statement import BankStatement
from pathlib import Path
import flask

app = flask.Flask(__name__)

@app.route("/")
def home():
    budget = Budget()
    sort_by = flask.request.args.get('sort_by', 'col2')
    order = flask.request.args.get('order', 'asc')
    date_filter = flask.request.args.get('date_filter', '2025-07')
    print(date_filter)
    valid_columns = {
        'col1': 'Name',  # Replace with your actual SQL column name
        'col2': 'Date',
        'col3': 'Amount',
        'col4': 'Category'
    }
    
    db_column = valid_columns.get(sort_by, 'Date')
    db_order = 'DESC' if order == 'desc' else 'ASC'

    result = budget.get_expenses_by_month_sql(date_filter, db_order, db_column)
    months = budget.get_distinct_months()
    summary = budget.summary(date_filter)

    return flask.render_template(
        "index.html", 
        expenses=result, 
        dates=months,       # The SQL list for the dropdown
        current_filter=date_filter,
        current_sort=sort_by, 
        current_order=order,
        summary=summary,
    )

@app.route("/table")
def about():
    # You can pass variables directly to your HTML template
    return flask.render_template("table.html", title="Expense Table")

import traceback

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        traceback.print_exc()
        print(f"Caught exception, see traceback below for details:\n {e}")
        sys.exit(1)
