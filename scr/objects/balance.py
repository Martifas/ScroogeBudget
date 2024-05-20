import csv
import os
import datetime
from scr.menu.utilities import menu_compiler
from scr.objects.username import read_profile_file
from scr.objects.stats import Stats


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
        message_string = f"{n} deposited"
        return message_string

    def expense(self, n: int) -> str:
        if n > self.balance:
            message_string = f"Balance ({self.balance}) is too low for the operation"
        else:
            self.balance -= n
            self.update_balance_savings("balance")
            message_string = f"{n} withdrawn"
        return message_string

    def balance_menu(self, message: str = None) -> None:
        modes = ["Income/Expense", "Current balance", "Savings"]
        output_string = "MAIN/BALANCE MENU"
        mode = menu_compiler(modes, output_string, message)
        if mode == "back":
            return
        self.select_balance_mode(mode)

    def select_balance_mode(self, mode: str) -> None:
        match mode:
            case "1" | "income" | "expense" | "i" | "e":
                message_string = self.validate_transaction()
            case "2" | "current balance":
                message_string = f"Current account balance: {self.balance}"
            case "3" | "budgeting":
                self.savings_menu()
                return
            case "back":
                return
            case _:
                message_string = "Error: incorrect input"
        if mode != "back":
            self.balance_menu(message_string)

    def savings_menu(self, message: str = None):
        modes = ["Deposit/withdraw", "Current savings balance", "Savings goal"]
        output_string = "MAIN/BALANCE/SAVINGS MENU"
        mode = menu_compiler(modes, output_string, message)
        if mode == "back":
            self.balance_menu()
        else:
            self.select_savings_mode(mode)

    def select_savings_mode(self, mode: str):
        match mode:
            case "1" | "deposit" | "withdraw" | "deposit/withdraw" | "d":
                message = self.savings_deposit_withdraw()
            case "2" | "current savings balance" | "c":
                message = f"Current savings accoung balance: {self.savings}"
            case "3" | "monthly savings goal" | "goal" | "m":
                message = self.calculate_savings()
            case "back":
                self.balance_menu()
                return
            case _:
                message = "Error: incorrect input"
        if mode != "back":
            self.savings_menu(message)

    def savings_deposit_withdraw(self) -> str:
        n = input("Would you like to deposit or withdraw?: ").strip().lower()
        if n == "deposit":
            self.amount = int(input("How much to deposit? "))
            if self.amount > self.balance:
                message = f"Account balance ({self.balance}) is too low for the operation"
                
            else:
                self.savings += self.amount    
                self.balance -= self.amount
                message = f"{self.amount} added to savings and removed from account"
                self.add_transactions(transaction_mode="savings")
                self.amount = 0 - self.amount
                self.add_transactions(transaction_mode="expense")

        elif n == "withdraw":
            self.amount = int(input("How much to withdraw?: "))
            if self.amount > self.savings:
                message = f"Not enough in savings account ({self.savings})"
    
            else:
                self.savings -= self.amount
                self.balance += self.amount
                message = f"{self.amount} taken from savings and added to account"
                self.add_transactions(transaction_mode="income")
                self.amount = 0 - self.amount
                self.add_transactions(transaction_mode="savings")
                
        else:
            message = "Error: incorrect input"
            
        
        self.update_balance_savings("savings")
        self.update_balance_savings("balance")
        return message


    def savings_goal(self) -> int:
        savings_goal = int(input("How much % of monthly income would you like to save? "))
        data = Stats(self.username).income_stats()[0]
        current_month = datetime.date.today().strftime("%Y-%m")
        if current_month in data:
            savings_goal_amount = int(data[current_month] * (savings_goal / 100))
            return int(savings_goal_amount)
        else:
            print("No data for this month")
            return

    def calculate_savings(self):
        savings_goal_amount = self.savings_goal()
        message = f"Saved this month: {self.savings}\nMonthly goal: {savings_goal_amount}\nAchieved: {int((self.savings/savings_goal_amount) * 100)}%"
        return message

    def validate_transaction(self) -> str:
        transaction_mode = input(f"Income or expense?: ").lower().strip()
        self.amount = input(f"Record amount: ")
        if transaction_mode == "back" or self.amount == "back":
            self.balance_menu()
        elif transaction_mode == "expense":
            message_string = self.expense(int(self.amount))
            self.add_transactions(transaction_mode) # TO DO
        elif transaction_mode == "income":
            message_string = self.income(int(self.amount))
            self.add_transactions(transaction_mode) # TO DO
        else:
            print("Enter 'income' or 'expense'")
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
