import csv
import sys
import re
import os
from typing import List, Tuple
from scr.locales import locale_en as locale
from scr.menu.utilities import message_compiler


def get_data_path() -> str:
    """
    Get the path to the data directory.

    Returns:
        str: The path to the data directory.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "..", "..", "data")


def create_profile_file(username: str) -> None:
    """
    Create a new profile file and transactions file for the specified username.

    Args:
        username (str): The username for which the profile and transactions files will be created.
    """
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


def read_profile_file(
    username: str, transactions: bool = False
) -> Tuple[List[List[str]], str]:
    """
    Read the profile file or transactions file for the specified username.

    Args:
        username (str): The username for which the profile or transactions file will be read.
        transactions (bool): Flag indicating whether to read the transactions file (True) or the profile file (False).

    Returns:
        Tuple[List[List[str]], str]: A tuple containing the profile or transactions data as a list of lists,
                                     and a message indicating the success or failure of the file read operation.
    """
    data_path = get_data_path()
    file_path = os.path.join(
        data_path,
        f"{'user_' if not transactions else ''}{username}{'_transactions' if transactions else ''}.csv",
    )

    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            profile_data = list(reader)
            message = (
                locale.USERNAME_SELECTED
                if not transactions
                else locale.USERNAME_TRANSACTIONS_SELECTED
            )
        return profile_data, message

    except FileNotFoundError:
        return [], locale.ERROR_FILE_NOT_FOUND


def profile_option() -> Tuple[int, str, str]:
    """
    Get the user's profile information.

    Returns:
        Tuple[int, str, str]: A tuple containing the user's balance, a message indicating the success or failure
                              of opening the profile, and the username.
    """
    username = get_profile()
    profile_data, message = open_profile(username)
    balance = int(profile_data[1][0])
    return balance, message, username


def get_profile() -> str:
    """
    Prompt the user to enter a valid username.

    Returns:
        str: The entered username.
    """
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
    """
    Prompt the user for a valid input based on the specified prompt.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        str: The user's valid input.
    """
    while True:
        user_input = input(prompt).lower().strip()

        if user_input in locale.USERNAME_VALID_INPUTS:
            return user_input
        else:
            print(locale.USERNAME_INVALID_INPUT)


def open_profile(username: str) -> Tuple[List[List[str]], str]:
    """
    Open the profile file for the specified username or create a new profile if it doesn't exist.

    Args:
        username (str): The username for which the profile file will be opened or created.

    Returns:
        Tuple[List[List[str]], str]: A tuple containing the profile data as a list of lists,
                                     and a message indicating the success or failure of opening the profile.
    """
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
