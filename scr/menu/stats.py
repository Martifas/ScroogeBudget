import scr.locales.locale_en as locale
from scr.menu.username import read_profile_file
from scr.menu.utilities import menu_compiler
import pandas as pd
from tabulate import tabulate

class Stats:
    def __init__(self, username: str):
        self.username: str = username
        self.transactions_data: list = read_profile_file(self.username, transactions=True)[0]
        
    def stats_menu(self, username: str) -> str:
        modes: list = locale.STATS_MODES
        stats_title: str = locale.STATS_TITLE
        mode: str = menu_compiler(modes, stats_title)
        if mode == locale.BACK:
            return username
        self.select_mode(mode)
        return username

    def select_mode(self, mode: str) -> None:
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

    def compile_stats(self, mode: str) -> str:
        filter_conditions = {
            "income/expense": lambda row: row[0] in locale.STATS_TRANSACTIONS_TYPES,
            "savings": lambda row: row[0] == locale.SAVINGS
        }
        if mode in filter_conditions:
            filtered_data: list = [row for row in self.transactions_data if filter_conditions[mode](row)]
            message_string: str = self.show_stats(filtered_data, mode)
        else:
            message_string: str = locale.ERROR_WRONG_INPUT
        return message_string

    def show_stats(self, data_list: list, mode: str) -> str:
        if mode == "income/expense":
            message: str = self.display_table(data_list, locale.STATS_INCOME_EXPENSE_TABLE, locale.STATS_INCOME_EXPENSE_DISPLAYED)
        elif mode == "savings":
            message: str = self.display_table(data_list, locale.STATS_SAVINGS_TABLE, locale.STATS_SAVINGS_TABLE_DISPLAYED)
        else:
            message: str = locale.ERROR_WRONG_INPUT
        return message

    def display_table(self, data_list: list, table_title: str, displayed_message: str) -> str:
        df: pd.DataFrame = pd.DataFrame(data_list, columns=["transaction_type", "date", "amount"])
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = pd.to_numeric(df["amount"])
        df["month"] = df["date"].dt.strftime("%Y-%m")
        pivot_df: pd.DataFrame = df.pivot_table(index="month", columns="transaction_type", values="amount", aggfunc="sum").fillna(0)
        table: str = tabulate(pivot_df, headers="keys", tablefmt="grid", floatfmt=".2f")
        print(table_title)
        print(table)
        print()
        return displayed_message