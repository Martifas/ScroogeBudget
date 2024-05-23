import csv
import sys
import re
import os
from typing import List, Tuple
from scr.locales import locale_en as locale
from scr.menu.utilities import message_compiler

def get_data_path() -> str:
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "..", "..", "data")

def create_profile_file(username: str) -> None:
    data_path = get_data_path()
    profile_file_path = os.path.join(data_path, f"user_{username}.csv")
    transactions_file_path = os.path.join(data_path, f"{username}_transactions.csv")

    try:
        with open(profile_file_path, "a", newline="") as file:
            writer: csv.writer = csv.writer(file)
            writer.writerow(["balance", "savings"])
            writer.writerow(["0", "0"])

        with open(transactions_file_path, "a", newline="") as another_file:
            writer: csv.writer = csv.writer(another_file)
            writer.writerow(["transaction_type", "date", "amount"])

    except OSError:
        print(locale.ERROR_CREATING_FILE)
        sys.exit(1)

def read_profile_file(username: str, transactions: bool = False) -> Tuple[List[List[str]], str]:
    data_path = get_data_path()
    file_path = os.path.join(data_path, f"{'user_' if not transactions else ''}{username}{'_transactions' if transactions else ''}.csv")

    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            profile_data = list(reader)
            message = locale.USERNAME_SELECTED if not transactions else locale.USERNAME_TRANSACTIONS_SELECTED
        return profile_data, message

    except FileNotFoundError:
        return [], locale.ERROR_FILE_NOT_FOUND

def profile_option() -> Tuple[int, str, str]:
    username = get_profile()
    profile_data, message = open_profile(username)
    balance = int(profile_data[1][0])
    return balance, message, username

def get_profile() -> str:
    message_string = locale.USERNAME_ENTER
    print(message_compiler(message_string))

    while True:
        username = input(locale.USERNAME).lower().strip()
        username_match = re.search(r"^\w+$", username)

        if username_match:
            break

        print(locale.ERROR_INCORRECT_FORMAT)

    return username

def get_valid_input(prompt: str) -> str:
    while True:
        user_input = input(prompt).lower().strip()

        if user_input in locale.USERNAME_VALID_INPUTS:
            return user_input
        else:
            print(locale.USERNAME_INVALID_INPUT)

def open_profile(username: str) -> Tuple[List[List[str]], str]:
    profile_data, message = read_profile_file(username)

    if message == locale.ERROR_FILE_NOT_FOUND:
        prompt = locale.USERNAME_NO_PROFILE
        new_user = get_valid_input(prompt)

        if new_user == locale.USERNAME_Y:
            create_profile_file(username)
            return open_profile(username)
        elif new_user == locale.USERNAME_N:
            sys.exit()

    return profile_data, message