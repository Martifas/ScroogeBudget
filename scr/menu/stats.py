import scr.locales.locale_en as locale
from scr.menu.username import read_profile_file
from scr.menu.utilities import menu_compiler
import pandas as pd
from tabulate import tabulate

class Stats:
    def __init__(self, username):
        self.username = username
        self.transactions_data = read_profile_file(self.username, transactions=True)[0]

    def stats_menu(self, username):
        modes = locale.STATS_MODES
        stats_title = locale.STATS_TITLE
        mode = menu_compiler(modes, stats_title)
        if mode == locale.BACK:
            return username
        self.select_mode(mode)
        return username

    def select_mode(self, mode):
        match mode:
            case _ if mode in locale.STATS_MODE_1:
                message_string: str = self.compile_stats("income/expense")
            case _ if mode in locale.STATS_MODE_2:
                message_string: str = self.compile_stats("savings")
            case _:
                message_string: str = locale.ERROR_WRONG_INPUT
        if mode != locale.BACK:
            print(message_string)
            self.stats_menu(self.username)

    def compile_stats(self, mode):
        if mode == "income/expense":
            filtered_data = [row for row in self.transactions_data if row[0] in ["income", "expense", "balance"]]
            message_string = self.show_stats(filtered_data, mode)
        elif mode == "savings":
            filtered_data = [row for row in self.transactions_data if row[0] == "savings"]
            message_string = self.show_stats(filtered_data, mode)
        else:
            message_string = locale.ERROR_WRONG_INPUT
        return message_string

    def show_stats(self, data_list, mode) -> str:
        if mode == "income/expense":
            message = self.display_income_expense_table(data_list)
        elif mode == "savings":
            message = self.display_savings_table(data_list)
        else:
            message = locale.ERROR_WRONG_INPUT
        return message

    def display_income_expense_table(self, data_list):
        df = pd.DataFrame(data_list, columns=['transaction_type', 'date', 'amount'])
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        df['month'] = df['date'].dt.strftime('%Y-%m')
        pivot_df = df.pivot_table(index='month', columns='transaction_type', values='amount', aggfunc='sum').fillna(0)

        table = tabulate(pivot_df, headers='keys', tablefmt='grid', floatfmt='.2f')
        print("\nIncome/Expense Table:")
        print(table)
        print()

        return "Income/Expense table displayed."

    def display_savings_table(self, data_list):
        df = pd.DataFrame(data_list, columns=['transaction_type', 'date', 'amount'])
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        df['month'] = df['date'].dt.strftime('%Y-%m')
        pivot_df = df.pivot_table(index='month', columns='transaction_type', values='amount', aggfunc='sum').fillna(0)

        table = tabulate(pivot_df, headers='keys', tablefmt='grid', floatfmt='.2f')
        print("\nSavings Table:")
        print(table)
        print()

        return "Savings table displayed."