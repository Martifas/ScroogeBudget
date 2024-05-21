import csv
import sys
import re
import os
from typing import List, Tuple
from scr.locales import locale_en as locale
from scr.menu.utilities import message_compiler

global username


def create_profile_file(username: str) -> None:
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, '..', '..', 'data')
    profile_file_path = os.path.join(data_path, f"user_{username}.csv")
    transactions_file_path = os.path.join(data_path, f"{username}_transactions.csv")

    try:
        with open(profile_file_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["balance", "savings"])
            writer.writerow(["0", "0"])
        with open(transactions_file_path, "a", newline="") as another_file:
            writer = csv.writer(another_file)
            writer.writerow(["transaction_type", "date", "amount"])
    except OSError:
        print(locale.ERROR_CREATING_FILE)
        sys.exit(1)

def read_profile_file(username: str, transactions: bool = False) -> Tuple[List[List[str]], str]:
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, '..', '..', 'data')

    try:
        if not transactions:
            file_path = os.path.join(data_path, f"user_{username}.csv")
        else:
            file_path = os.path.join(data_path, f"{username}_transactions.csv")

        with open(file_path, "r") as file:
            reader = csv.reader(file)
            profile_data = list(reader)
            message = "profile selected" if not transactions else "transactions file selected"


        return profile_data, message

    except FileNotFoundError:
        return [], "file not found"

def profile_option():
    username = get_profile()
    profile_data = Profile(username).open_profile()[0]
    balance = int(profile_data[1][0])
    message = "Profile selected"
    return balance, message, username

def get_profile() -> str:
    message_string : str = "ENTER YOUR USERNAME"
    print(message_compiler(message_string))
    while True:
        global username
        username = input("Username: ").lower().strip()
        username_match = re.search(r"^\w+$", username)
        if username_match:
            break
        print("Incorrect format")
    return username



def get_valid_input(prompt: str) -> str:
    while True:
        user_input = input(prompt).lower().strip()
        if user_input in ("y", "n", "yes", "no"):
            return user_input
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

class Profile:
    def __init__(self, username: str) -> None:
        self.username: str = username

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        self._username: str = username

    def open_profile(self) -> Tuple[List[List[str]], str]:
        profile_data, message = read_profile_file(self.username)

        if message == "file not found":
            prompt = "No profile found. Create new profile? (y/n): "
            new_user = get_valid_input(prompt)

            if new_user == "y":
                create_profile_file(self.username)
                return self.open_profile()
            elif new_user == "n":
                sys.exit()

        return profile_data, message
