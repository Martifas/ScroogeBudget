import csv
import os
import datetime
import scr.locales.locale_en as locale
from scr.menu.utilities import menu_compiler
from scr.menu.username import read_profile_file
from typing import List, Optional


class Balance:
    def __init__(self, username: str) -> None:
        self.username = username
        self.profile_data: List[List[str]] = read_profile_file(self.username)[0]
        self.savings = int(self.profile_data[1][1])
        self.balance = int(self.profile_data[1][0])
        base_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_path, "..", "..", "data")
        self.profile_file_path = os.path.join(data_path, f"user_{self.username}.csv")
        self.transactions_file_path = os.path.join(
            data_path, f"{self.username}_transactions.csv"
        )
        self.transactions_data = read_profile_file(self.username, transactions=True)[0]

    def balance_menu(self, message: Optional[str] = None) -> None:
        modes = locale.BALANCE_MODES
        balance_title = locale.BALANCE_TITLE
        mode = menu_compiler(modes, balance_title, message)
        if mode == locale.BACK:
            return
        self.select_balance_mode(mode)

    def select_balance_mode(self, mode: str) -> None:
        from scr.menu.savings import Savings

        match mode:
            case _ if mode in locale.BALANCE_MODE_1:
                message_string = self.validate_transaction()
                if message_string == locale.BACK:
                    self.balance_menu()
                    return
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
            return locale.BACK

        if transaction_mode != locale.INCOME and transaction_mode != locale.EXPENSE:
            return locale.BALANCE_ERROR_VALIDATE

        amount = input(locale.BALANCE_RECORD_AMOUNT)
        if amount == locale.BACK:
            return locale.BACK

        try:
            self.amount = int(amount)
        except ValueError:
            return locale.BALANCE_ERROR_VALIDATE

        if transaction_mode == locale.EXPENSE:
            message_string = self.expense(self.amount)
        else:
            message_string = self.income(self.amount)

        return message_string

    def income(self, n: int) -> str:
        self.balance += n
        self.update_balance_savings("balance")
        self.add_transactions("income", n)
        self.update_balance_in_transactions(n)
        message_string = str(n) + locale.BALANCE_DEPOSIT
        return message_string

    def expense(self, n: int) -> str:
        if n > self.balance:
            message_string: str = locale.BALANCE_TOO_LOW + str(self.balance)
        else:
            self.balance -= n
            self.update_balance_savings("balance")
            self.add_transactions("expense", n)
            updated_n = -n
            self.update_balance_in_transactions(updated_n)
            message_string = str(n) + locale.BALANCE_WITHDRAWN
        return message_string

    def update_balance_savings(self, n: str) -> None:
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

    def add_transactions(self, transaction_mode: str, amount: int) -> None:
        current_date = datetime.date.today().strftime(locale.YEAR_MONTH)
        transaction_found: bool = False
        try:
            with open(self.transactions_file_path, "r", newline="") as file:
                reader = csv.reader(file)
                rows = list(reader)
        except FileNotFoundError:
            rows = []

        for row in rows:
            if row[1] == current_date and transaction_mode == row[0]:
                existing_amount = row[2]
                row[2] = str(int(existing_amount) + amount)
                transaction_found = True
                break
        if not transaction_found:
            rows.append([transaction_mode, current_date, str(amount)])
        with open(self.transactions_file_path, "w", newline="") as write_file:
            writer = csv.writer(write_file)
            writer.writerows(rows)

    def update_balance_in_transactions(self, n: int) -> None:
        current_date = datetime.date.today().strftime(locale.YEAR_MONTH)
        transaction_found: bool = False
        try:
            with open(self.transactions_file_path, "r", newline="") as file:
                reader = csv.reader(file)
                rows = list(reader)
        except FileNotFoundError:
            rows = []

        for row in rows:
            if row[1] == current_date and row[0] == "balance":
                temporary_amount = int(row[2]) + n
                row[2] = str(temporary_amount)
                transaction_found = True
                break
        if not transaction_found:
            rows.append(["balance", current_date, str(temporary_amount)])
        with open(self.transactions_file_path, "w", newline="") as write_file:
            writer = csv.writer(write_file)
            writer.writerows(rows)
