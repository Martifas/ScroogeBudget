import scr.locales.locale_en as locale
import datetime
from utilities import menu_compiler

class Savings:
    def __init__(self):
        pass

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
                self.amount = -self.amount
                self.add_transactions(transaction_mode="income")

        elif n == locale.WITHDRAW:
            self.amount = int(input(locale.SAVINGS_AMOUNT_WITHDRAW))
            if self.amount > self.savings:
                message = locale.SAVINGS_TOO_LOW + str(self.savings)

            else:
                self.savings -= self.amount
                self.balance += self.amount
                message = str(self.amount) + locale.SAVINGS_REMOVED_BALANCE_ADDED
                self.add_transactions(transaction_mode="income")
                self.amount = -self.amount
                self.add_transactions(transaction_mode="savings")

        else:
            message = locale.ERROR_WRONG_INPUT

        self.update_balance_savings("savings")
        self.update_balance_savings("balance")
        return message

    def get_transaction_amount(self, mode: str) -> str:
        current_month = datetime.date.today().strftime(locale.YEAR_MONTH)
        for row in self.transactions_data:
            if row[0] == mode and row[1] == current_month:
                return row[2]
        message = message = locale.ERROR_NO_DATA
        self.savings_menu(message=message)

    def example(self) -> int: #review names of functions
        try:
            savings_goal_percent = input(locale.SAVINGS_GOAL_PERCENTAGE)
            if savings_goal_percent == locale.BACK:
                self.savings_menu()
            monthly_income = int(self.get_transaction_amount("income"))
            monthly_savings_goal = int(
                monthly_income * (int(savings_goal_percent) / 100)
            )
            return monthly_savings_goal

        except ValueError:
            message = locale.ERROR_WRONG_INPUT
            self.savings_menu(message=message)

    def calculate_savings(self):
        monthly_savings_goal = self.example()
        monthly_savings = monthly_savings = int(self.get_transaction_amount("savings"))
        message = (
            f"{locale.SAVINGS_THIS_MONTH}: {monthly_savings}\n"
            f"{locale.SAVINGS_GOALS_MESSAGE}: {monthly_savings_goal}\n"
            f"{locale.SAVINGS_ACHIEVED}: {int((monthly_savings / monthly_savings_goal) * 100)}%"
        )
        return message