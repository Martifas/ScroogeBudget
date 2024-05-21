import csv
from typing import List, Tuple
from pathlib import Path
import re


separator = "-"
case_chgr = "upper"


def select_separator() -> str:
    global separator
    user_input = input("Select one character to use as separator in menu: ")
    separator_match = re.search(r"^.$", user_input)
    if separator_match:
        separator = user_input
        message = f"Separator {separator} set"
    else:
        message = "Error: input 1 any character"

    return message


def case_changer() -> str:
    global case_chgr
    case = input(
        "Do you want the messages to be in lowercase, uppercase or titlecase?: "
    ).lower()
    if case == "lowercase":
        case_chgr = "lower"
    elif case == "uppercase":
        case_chgr = "upper"
    elif case == "titlecase":
        case_chgr = "title"
    else:
        print("Invalid input, setting to uppercase by default.")
        case_chgr = "upper"
    return case


def message_compiler(message_string: str) -> str:
    global separator, case_chgr
    if case_chgr == "upper":
        message_string = message_string.upper()
    elif case_chgr == "title":
        message_string = message_string.title()
    else:
        message_string = message_string.lower()
    message = f"{len(message_string) * separator}\n{message_string}\n{len(message_string) * separator}"
    return message


def menu_compiler(modes, output_string, message=None) -> str:
    output = [message_compiler(output_string)]
    for index, value in enumerate(modes, start=1):
        output.append(f"{index}. {value}")
        menu = "\n".join(output)
    print(menu)
    if message is not None:
        print(message_compiler(message))
    mode = input("SELECT MODE: ").lower().strip()
    return mode
