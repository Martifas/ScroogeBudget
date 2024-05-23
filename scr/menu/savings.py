import scr.locales.locale_en as locale
import datetime
from scr.menu.utilities import menu_compiler
from scr.menu.username import read_profile_file
from scr.menu.forecast import forecast_menu
from typing import Optional, Union

class Savings:
    def __init__(self, username: str) -> None:
        self.username = username
        self.profile_data = read_profile_file(self.username)[0]
        self.savings = int(self.profile_data[1][1])
        self.balance = int(self.profile_data[1][0])
        from scr.menu.balance import Balance
        self.Balance = Balance(self.username)
        self.transactions_data = read_profile_file(self.username, transactions=True)[0]

    def savings_menu(self, message: Optional[str] = None) -> None:
        modes = locale.SAVINGS_MODES
        savings_title: str = locale.SAVINGS_TITLE
        mode = menu_compiler(modes, savings_title, message)
        if mode == locale.BACK:
            self.Balance.balance_menu()
        else:
            self.select_savings_mode(mode)

    def select_savings_mode(self, mode: str) -> None:
        match mode:
            case _ if mode in locale.SAVINGS_MODE_1:
                message: str = self.savings_deposit_withdraw()
            case _ if mode in locale.SAVINGS_MODE_2:
                message = locale.SAVINGS_BALANCE + str(self.savings)
            case _ if mode in locale.SAVINGS_MODE_3:
                message = self.calculate_savings()
            case _ if mode in locale.SAVINGS_MODE_4:
                message = forecast_menu(self.username)
            case locale.BACK:
                self.Balance.balance_menu()
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
                self.Balance.add_transactions(transaction_mode="savings", amount=self.amount)
                self.Balance.add_transactions(transaction_mode="balance", amount=-self.amount)
        elif n == locale.WITHDRAW:
            self.amount = int(input(locale.SAVINGS_AMOUNT_WITHDRAW))
            if self.amount > self.savings:
                message = locale.SAVINGS_TOO_LOW + str(self.savings)
            else:
                self.savings -= self.amount
                self.balance += self.amount
                message = str(self.amount) + locale.SAVINGS_REMOVED_BALANCE_ADDED
                self.Balance.add_transactions(transaction_mode="balance", amount=self.amount)
                self.amount = -self.amount
                self.Balance.add_transactions(transaction_mode="savings", amount=self.amount)
        else:
            message = locale.ERROR_WRONG_INPUT

        self.Balance.balance = self.balance
        self.Balance.savings = self.savings
        self.Balance.update_balance_savings("savings")
        self.Balance.update_balance_savings("balance")
        return message

    def get_transaction_amount(self, mode: str) -> Union[str, int]:
        current_month = datetime.date.today().strftime(locale.YEAR_MONTH)
        for row in self.transactions_data:
            if row[0] == mode and row[1] == current_month:
                return float(row[2])
        message = locale.ERROR_NO_DATA
        self.savings_menu(message=message)
        return message

    def goal_getter(self) -> Optional[int]:
        try:
            savings_goal_percent = input(locale.SAVINGS_GOAL_PERCENTAGE)
            if savings_goal_percent == locale.BACK:
                self.savings_menu()
            monthly_income = self.get_transaction_amount("income")
            monthly_savings_goal = float(monthly_income * (float(savings_goal_percent) / 100))
            return monthly_savings_goal
        except ValueError:
            message = locale.ERROR_WRONG_INPUT
            self.savings_menu(message=message)
            return None

    def calculate_savings(self) -> str:
        monthly_savings_goal = self.goal_getter()
        if monthly_savings_goal is None:
            return locale.ERROR_WRONG_INPUT

        monthly_savings = float(self.get_transaction_amount("savings"))
        if isinstance(monthly_savings, str):
            return monthly_savings

        try:
            percentage_achieved = float((monthly_savings / monthly_savings_goal) * 100)
        except ZeroDivisionError:
            return locale.ERROR_INCOME_ZERO
        message = (
            f"{locale.SAVINGS_THIS_MONTH}: {monthly_savings} | {locale.SAVINGS_GOALS_MESSAGE}: {monthly_savings_goal:.2f} | {locale.SAVINGS_ACHIEVED}: {percentage_achieved:.2f}%"
        )
        return message
