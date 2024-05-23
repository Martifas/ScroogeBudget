BACK = "back"
DEPOSIT = "deposit"
WITHDRAW = "withdraw"
EXPENSE = "expense"
INCOME = "income"
BALANCE = "balance"
SAVINGS = "savings"
INCOME_EXPENSE = f"{INCOME} or {EXPENSE}? "

BALANCE_MODES = ["Income/Expense", "Current balance", "Savings"]
BALANCE_TITLE = "main/balance menu"
BALANCE_DEPOSIT = " deposited"
BALANCE_TOO_LOW = "account balance is too low of the operation: "
BALANCE_WITHDRAWN = ' withdrawn'
BALANCE_BALANCE = "current account balance: "
BALANCE_MODE_1 = ("1", "income", "expense", "i", "e")
BALANCE_MODE_2 = ("2", "current balance", "c")
BALANCE_MODE_3 = ("3", "savings")
BALANCE_RECORD_AMOUNT = "Record amount: "
BALANCE_ERROR_VALIDATE = "Enter 'income' or 'expense'"
MENU_MODES = ["Balance & Savings", "Statistics", "Profile", "Options", "Exit"]
MENU_TITLE = "MAIN MENU"
SELECT_MODE = "Select mode: "
MENU_HANDLING_MODES = ["1", "2", "3", "4", "5", "budget", "statistics", "profile", "options", "exit"]
MENU_HANDLING_MODES_WITHOUT_PROFILE = ["3", "profile", "4", "options", "5", "exit"]
MENU_HANDLING_USER = "Select user first"
MODE_SELECT_BALANCE_1 = ("1", "balance", "savings", "b")
MODE_SELECT_STATISTICS_2 = ("2", "statistics", "s")
MODE_SELECT_PROFILE_3 = ("3", "profile", "p")
MODE_SELECT_OPTIONS_4 = ("4", "options", "o")
MODE_SELECT_EXIT_5 = ("5", "exit", "e")

ERROR_WRONG_INPUT = "Error: wrong input"
ERROR_CREATING_FILE = "Error creating profile file"
ERROR_INCORRECT_FORMAT = "Incorrect format"
ERROR_NO_DATA = "no data for this month"
ERROR_FILE_NOT_FOUND = "file not found"
ERROR_INCOME_ZERO = "No income this month"

FORECAST_MODES = ["Date when wanted savings amount could be reached", "Amount of savings on specific date"]
FORECAST_TITLE = "Forecast menu"
FORECAST_SELECT_MODE_1 = ("1", "date", "d")
FORECAST_SELECT_MODE_2 = ("2", "amount", "a")
FORECAST_ERROR_NO_DATA = "Data missing for forecast"
FORECAST_AMOUNT_WANTED = "What amount of savings would you like to have? "
FORECAST_DATE_WANTED = "Enter the target date (YYYY-MM): "
FORECAST_INVALID_FORMAT = "Invalid date format. Please enter the date in the format YYYY-MM."
FORECAST_NO_LOWER_DATE = "Target date cannot be lower than today's date."
FORECAST_DATE_BASED = "Based on your average monthly savings of "
FORECAST_REACH_GOAL = "You will reach your savings goal "
FORECAST_APPROXIMATELY = "Which is approximately "
FORECAST_ALREADY_HAVE = "You already have in savings: "
FORECAST_SAVINGS = "your forecasted savings amount on "
FORECAST_IS_APPROXIMATELY = "is approximately"
FORECAST_IN = "in"
FORECAST_MONTHS = "months"

MAIN_EXIT = "|PROGRAM CLOSED|"

OPTIONS_MODES = ["Change message/error separator", "Change messages to uppercase, lowercase or titlecase"]
OPTIONS_TITLE = "OPTIONS"
OPTIONS_ERROR = "Error: Select by entering '1' or '2'"

UTILITIES_SEPARATOR_INPUT = "Select one character to use as separator in menu: " 
UTILITIES_SEPARATOR_SET = "Separator set: "
UTILITIES_SEPARATOR_ERROR = "Error: input 1 of any character"
UTILITIES_CASE_INPUT = "Do you want the messages to be in lowercase, uppercase or titlecase?: "
UTILITIES_LOWERCASE = "lowercase"
UTILITIES_UPPERCASE = "uppercase"
UTILITIES_TITLECASE = "titlecase"
UTILITIES_SET_TO_LOWERCASE = "Messages set to lowercase "
UTILITIES_SET_TO_TITLECASE = "Messages set to titlecase "
UTILITIES_SET_TO_UPPERCASE = "Messages set to uppercase "
UTILITIES_CASE_ERROR = "Error: invalid input, setting to uppercase by default"

SAVINGS_MODES = ["Deposit/withdraw", "Current savings balance", "Savings goal", "Forecast"]
SAVINGS_TITLE = "main/balance/savings menu"
SAVINGS_BALANCE = "current savings account balance: "
SAVINGS_MODE_1 = ("1", "deposit", "withdraw", "deposit/withdraw", "d", "w")
SAVINGS_MODE_2 = ("2", "current savings balance", "c")
SAVINGS_MODE_3 =  ("3", "monthly savings goal", "goal", "m")
SAVINGS_MODE_4 = ("4", "forecast", "f")
SAVINGS_DEPOSIT_WITHDRAW = "Would you like to deposit or withdraw?: "
SAVINGS_AMOUNT_DEPOSIT = "how much to deposit? "
SAVINGS_AMOUNT_WITHDRAW = "how much to withdraw? "
SAVINGS_TOO_LOW = "savings balance is too low of the operation: "
SAVINGS_ADDED_BALANCE_REMOVED = " added to savings and removed from account"
SAVINGS_REMOVED_BALANCE_ADDED = " taken from savings and added to account"
SAVINGS_GOAL_PERCENTAGE = "How much % of monthly income would you like to save? "
SAVINGS_THIS_MONTH = "Saved this month"
SAVINGS_ACHIEVED = "Achieved"
SAVINGS_GOALS_MESSAGE = 'Monthly goal'

STATS_MODES = ["Income/expense stats", "Savings stats"]
STATS_MODE_1 = ("1", "income", "expense", "income/expense stats", "i")
STATS_MODE_2 = ("2", "savings stats", "s")
STATS_TRANSACTIONS_TYPES = ["income", "expense", "balance"]
STATS_TITLE = "statistics menu"
STATS_INCOME_EXPENSE_TABLE = f"\nIncome/Expense Table:"
STATS_SAVINGS_TABLE = "\nSavings table:"
STATS_SAVINGS_TABLE_DISPLAYED = "Savings table displayed"
STATS_INCOME_EXPENSE_DISPLAYED = f"Income/Expense table displayed"
STATS_SHOWING = "Showing stats in browser"
YEAR_MONTH = "%Y-%m"

USERNAME = "Username: "
USERNAME_ENTER = "Enter your username"
USERNAME_VALID_INPUTS = ("y", "n", "yes", "no")
USERNAME_INVALID_INPUT = "Error: please enter 'y' or 'n'."
USERNAME_NO_PROFILE = "No profile found. Create new profile? (y/n): "
USERNAME_Y = "y"
USERNAME_N = "n"
USERNAME_SELECTED = "profile selected"
USERNAME_TRANSACTIONS_SELECTED = "transactions file selected"


