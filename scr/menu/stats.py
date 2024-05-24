import scr.locales.locale_en as locale
from scr.menu.username import read_profile_file
from scr.menu.utilities import menu_compiler
import pandas as pd
from tabulate import tabulate


class Stats:
    """
    Represents the statistics functionality.
    It generates and displays income/expense statistics and savings statistics for a specific user.
    """
    def __init__(self, username: str) -> None:
        self.username = username
        self.transactions_data = read_profile_file(self.username, transactions=True)[0]

    def stats_menu(self, username: str) -> str:
        modes = locale.STATS_MODES
        stats_title = locale.STATS_TITLE
        mode = menu_compiler(modes, stats_title)
        if mode == locale.BACK:
            return username
        self.select_mode(mode)
        return username

    def select_mode(self, mode: str) -> None:
        match mode:
            case _ if mode in locale.STATS_MODE_1:
                message_string = self.compile_stats("income/expense")
            case _ if mode in locale.STATS_MODE_2:
                message_string = self.compile_stats("savings")
            case _:
                message_string = locale.ERROR_WRONG_INPUT
        if mode != locale.BACK:
            print(message_string)
            self.stats_menu(self.username)

    def compile_stats(self, mode: str) -> str:
        """
        Compiles the statistics data based on the selected mode (income/expense or savings).

        Args:
            mode (str): The mode of the statistics (income/expense or savings).

        Returns:
            str: A message indicating the result of compiling the statistics.
        """
        filter_conditions = {
            "income/expense": lambda row: row[0] in locale.STATS_TRANSACTIONS_TYPES,
            "savings": lambda row: row[0] == locale.SAVINGS,
        }
        if mode in filter_conditions:
            filtered_data = [
                row for row in self.transactions_data if filter_conditions[mode](row)
            ]
            message_string = self.show_stats(filtered_data, mode)
        else:
            message_string = locale.ERROR_WRONG_INPUT
        return message_string

    def show_stats(self, data_list: list, mode: str) -> str:
        """
        Displays the statistics data in a formatted table based on the selected mode.

        Args:
            data_list (list): The list of statistics data.
            mode (str): The mode of the statistics (income/expense or savings).

        Returns:
            str: A message indicating the result of displaying the statistics table.
        """
        if mode == "income/expense":
            message = self.display_table(
                data_list,
                locale.STATS_INCOME_EXPENSE_TABLE,
                locale.STATS_INCOME_EXPENSE_DISPLAYED,
            )
        elif mode == "savings":
            message = self.display_table(
                data_list,
                locale.STATS_SAVINGS_TABLE,
                locale.STATS_SAVINGS_TABLE_DISPLAYED,
            )
        else:
            message = locale.ERROR_WRONG_INPUT
        return message

    def display_table(
        self, data_list: list, table_title: str, displayed_message: str
    ) -> str:
        """
        Displays the statistics data in a formatted table using pandas and tabulate.

        Args:
            data_list (list): The list of statistics data.
            table_title (str): The title of the statistics table.
            displayed_message (str): The message to be displayed after the table is shown.

        Returns:
            str: The displayed message.
        """
        df = pd.DataFrame(data_list, columns=["transaction_type", "date", "amount"])
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = pd.to_numeric(df["amount"])
        df["month"] = df["date"].dt.strftime("%Y-%m")
        pivot_df = df.pivot_table(
            index="month", columns="transaction_type", values="amount", aggfunc="sum"
        ).fillna(0)
        table = tabulate(pivot_df, headers="keys", tablefmt="grid", floatfmt=".2f")
        print(table_title)
        print(table)
        print()
        return displayed_message
