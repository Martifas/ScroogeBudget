import csv
import os
import datetime
import scr.locales.locale_en as locale
from scr.menu.utilities import menu_compiler
from scr.menu.username import read_profile_file
from scr.menu.stats import Stats


class Balance:
    def __init__(self, username):
        self.username = username
        self.profile_data = read_profile_file(self.username)[0]
        self.savings = int(self.profile_data[1][1])
        self.balance = int(self.profile_data[1][0])
        base_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_path, '..', '..', 'data')
        self.profile_file_path = os.path.join(data_path, f"user_{self.username}.csv")
        self.transactions_file_path = os.path.join(data_path, f"{self.username}_transactions.csv")

    def income(self, n: int) -> str:
        self.balance += n
        self.update_balance_savings("balance")
        message_string = str(n) + locale.BALANCE_DEPOSIT
        return message_string

    def expense(self, n: int) -> str:
        if n > self.balance:
            message_string = locale.BALANCE_TOO_LOW + self.balance
        else:
            self.balance -= n
            self.update_balance_savings("balance")
            message_string = str(n) + locale.BALANCE_WITHDRAWN
        return message_string

    def balance_menu(self, message: str = None) -> None:
        modes = locale.BALANCE_MODES
        balance_title = locale.BALANCE_TITLE
        mode = menu_compiler(modes, balance_title, message)
        if mode == locale.BACK:
            return
        self.select_balance_mode(mode)

    def select_balance_mode(self, mode: str) -> None:
        match mode:
            case _ if mode in  locale.BALANCE_MODE_1:
                message_string = self.validate_transaction()
            case _ if mode in locale.BALANCE_MODE_2:
                message_string = locale.BALANCE_BALANCE + str(self.balance)
            case _ if mode in locale.BALANCE_MODE_3:
                self.savings_menu()
                return
            case locale.BACK:
                return
            case _:
                message_string = locale.ERROR_WRONG_INPUT
        if mode != locale.BACK:
            self.balance_menu(message_string)

    def savings_menu(self, message: str = None):
        modes = locale.SAVINGS_MODES
        savings_title = locale.SAVINGS_TITLE
        mode = menu_compiler(modes, savings_title, message)
        if mode == locale.BACK:
            self.balance_menu()
        else:
            self.select_savings_mode(mode)

    def select_savings_mode(self, mode: str):
        match mode:
            case _ if mode in locale.SAVINGS_MODE_1:
                message = self.savings_deposit_withdraw()
            case _ if mode in locale.SAVINGS_MODE_2:
                message = locale.SAVINGS_BALANCE + str(self.savings)
            case _ if mode in locale.SAVINGS_MODE_3:
                message = self.calculate_savings()
            case locale.BACK:
                self.balance_menu()
                return
            case _:
                message = locale.ERROR_WRONG_INPUT
        if mode != locale.BACK:
            self.savings_menu(message)

    def savings_deposit_withdraw(self) -> str:
        n = input(locale.SAVINGS_DEPOSIT_WITHDRAW).strip().lower()
        if n == locale.BACK:
            self.savings_menu()
        elif n == locale.DEPOSIT:
            self.amount = int(input(locale.SAVINGS_AMOUNT_DEPOSIT))
            if self.amount > self.balance:
                message = locale.BALANCE_TOO_LOW + str(self.balance)
                
            else:
                self.savings += self.amount    
                self.balance -= self.amount
                message = str(self.amount) + locale.SAVINGS_ADDED_BALANCE_REMOVED
                self.add_transactions(transaction_mode="savings")
                self.amount = 0 - self.amount
                self.add_transactions(transaction_mode="expense")

        elif n == locale.WITHDRAW:
            self.amount = int(input(locale.SAVINGS_AMOUNT_WITHDRAW))
            if self.amount > self.savings:
                message = locale.SAVINGS_TOO_LOW + self.savings
    
            else:
                self.savings -= self.amount
                self.balance += self.amount
                message = str(self.amount) + locale.SAVINGS_REMOVED_BALANCE_ADDED
                self.add_transactions(transaction_mode="income")
                self.amount = 0 - self.amount
                self.add_transactions(transaction_mode="savings")
                
        else:
            message = locale.ERROR_WRONG_INPUT
            
        
        self.update_balance_savings("savings")
        self.update_balance_savings("balance")
        return message


    def savings_goal(self) -> int:
        try:
            savings_goal = input(locale.SAVINGS_GOAL_PERCENTAGE)
            if savings_goal == locale.BACK:
                self.savings_menu()
            else:
                data = Stats(self.username).income_stats()[0]
                current_month = datetime.date.today().strftime(locale.YEAR_MONTH)
                if current_month in data:
                    savings_goal_amount = int(data[current_month] * (savings_goal / 100))
                    return int(savings_goal_amount)
                else:
                    print(locale.ERROR_NO_DATA)
                    self.savings_goal()
        except (TypeError, ValueError):
            print(locale.ERROR_WRONG_INPUT)
            self.savings_goal()

    def calculate_savings(self):
        savings_goal_amount = self.savings_goal()
        message = (f"{locale.SAVINGS_THIS_MONTH}: {self.savings}\n"
           f"{locale.SAVINGS_THIS_MONTH}: {savings_goal_amount}\n"
           f"{locale.SAVINGS_ACHIEVED}: {int((self.savings / savings_goal_amount) * 100)}%")
        return message
        

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
            print(locale.BALANCE_ERROR_VALIDATE)
            self.validate_transaction()
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
        with open(self.transactions_file_path, "r", newline="") as file:
            reader = csv.reader(file)
            rows = list(reader)

        rows.append(
            [
                f"{transaction_mode.title()}",
                datetime.date.today(),
                self.amount,
            ]
        )

        with open(self.transactions_file_path, "w", newline="") as write_file:
            writer = csv.writer(write_file)
            writer.writerows(rows)
