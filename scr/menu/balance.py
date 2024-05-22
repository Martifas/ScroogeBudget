import csv
import os
import datetime
import scr.locales.locale_en as locale
from scr.menu.utilities import menu_compiler
from scr.menu.username import read_profile_file

class Balance:
    def __init__(self, username):
        self.username = username
        self.profile_data = read_profile_file(self.username)[0]
        self.savings = int(self.profile_data[1][1])
        self.balance = int(self.profile_data[1][0])
        base_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_path, "..", "..", "data")
        self.profile_file_path = os.path.join(data_path, f"user_{self.username}.csv")
        self.transactions_file_path = os.path.join(data_path, f"{self.username}_transactions.csv")
        self.transactions_data = read_profile_file(self.username, transactions=True)[0]

    def income(self, n: int) -> str:
        self.balance += n
        self.update_balance_savings("balance")
        message_string = str(n) + locale.BALANCE_DEPOSIT
        return message_string

    def expense(self, n: int) -> str:
        if n > self.balance:
            message_string = locale.BALANCE_TOO_LOW + str(self.balance)
        else:
            self.balance -= n
            self.update_balance_savings("balance")
            message_string = str(n) + locale.BALANCE_WITHDRAWN
        return message_string

    def balance_menu(self, message: str = None) -> None:
        from scr.menu.savings import Savings  # Import here to avoid circular import at module level
        modes = locale.BALANCE_MODES
        balance_title = locale.BALANCE_TITLE
        mode = menu_compiler(modes, balance_title, message)
        if mode == locale.BACK:
            return
        self.select_balance_mode(mode)

    def select_balance_mode(self, mode: str) -> None:
        from scr.menu.savings import Savings  # Import here to avoid circular import at module level
        match mode:
            case _ if mode in locale.BALANCE_MODE_1:
                message_string = self.validate_transaction()
            case _ if mode in locale.BALANCE_MODE_2:
                message_string = locale.BALANCE_BALANCE + str(self.balance)
            case _ if mode in locale.BALANCE_MODE_3:
                Savings(self.username).savings_menu()
                return
            case locale.BACK:
                return
            case _:
                message_string = locale.ERROR_WRONG_INPUT
        if mode != locale.BACK:
            self.balance_menu(message_string)

    def validate_transaction(self) -> str:
        transaction_mode = input(locale.INCOME_EXPENSE).lower().strip()
        if transaction_mode == locale.BACK:
            self.balance_menu()
        self.amount = input(locale.BALANCE_RECORD_AMOUNT)
        if self.amount == locale.BACK:
            self.balance_menu()
        elif transaction_mode == locale.EXPENSE:
            message_string = self.expense(int(self.amount))
            self.add_transactions(transaction_mode)
        elif transaction_mode == locale.INCOME:
            message_string = self.income(int(self.amount))
            self.add_transactions(transaction_mode)
        else:
            message_string = locale.BALANCE_ERROR_VALIDATE
        return message_string

    def update_balance_savings(self, n) -> None:
        with open(self.profile_file_path, "r", newline="") as file:
            reader = csv.reader(file)
            rows = list(reader)
            if n == "balance":
                rows[1][0] = str(self.balance)
            else:
                rows[1][1] = str(self.savings)
            with open(self.profile_file_path, "w", newline="") as write_file:
                writer = csv.writer(write_file)
                writer.writerows(rows)

    def add_transactions(self, transaction_mode: str) -> None:
        current_date = datetime.date.today().strftime(locale.YEAR_MONTH)
        transaction_found = False
        try:
            with open(self.transactions_file_path, "r", newline="") as file:
                reader = csv.reader(file)
                rows = list(reader)
        except FileNotFoundError:
            rows = []
        for row in rows:
            if row[1] == current_date and transaction_mode == row[0]:
                existing_amount = row[2]
                row[2] = str(int(existing_amount) + int(self.amount))
                transaction_found = True
                break
        if not transaction_found:
            rows.append([transaction_mode, current_date, str(self.amount)])
        with open(self.transactions_file_path, "w", newline="") as write_file:
            writer = csv.writer(write_file)
            writer.writerows(rows)
