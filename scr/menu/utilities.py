import re
import scr.locales.locale_en as locale


separator = "-"
case_chgr = "upper"


def select_separator() -> str:
    """
    Prompt the user to select a separator character for the menu.

    Returns:
        str: A message indicating the selected separator or an error message if an invalid separator is entered.
    """
    global separator
    user_input = input(locale.UTILITIES_SEPARATOR_INPUT)
    separator_match = re.search(r"^.$", user_input)
    if separator_match:
        separator = user_input
        message = locale.UTILITIES_SEPARATOR_SET + separator
    else:
        message = locale.UTILITIES_SEPARATOR_ERROR

    return message


def case_changer() -> str:
    """
    Prompt the user to select the case style for the messages (lowercase, uppercase, or titlecase).

    Returns:
        str: A message indicating the selected case style or an error message if an invalid case style is entered.
    """
    global case_chgr
    case = input(locale.UTILITIES_CASE_INPUT).lower()
    if case == locale.UTILITIES_LOWERCASE:
        case_chgr = "lower"
        message = locale.UTILITIES_SET_TO_LOWERCASE
    elif case == locale.UTILITIES_UPPERCASE:
        case_chgr = "upper"
        message = locale.UTILITIES_SET_TO_UPPERCASE
    elif case == locale.UTILITIES_TITLECASE:
        case_chgr = "title"
        message = locale.UTILITIES_SET_TO_TITLECASE
    else:
        message = locale.UTILITIES_CASE_ERROR
        case_chgr = "upper"
    return message


def message_compiler(message_string: str) -> str:
    """
    Compile the message string with the selected case style and separator.

    Args:
        message_string (str): The message string to be compiled.

    Returns:
        str: The compiled message string with the selected case style and separator.
    """
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
    """
    Compile the menu options and display the menu.

    Args:
        modes: The list of menu options.
        output_string: The output string for the menu.
        message (optional): An optional message to be displayed with the menu.

    Returns:
        str: The user's selected mode.
    """
    output = [message_compiler(output_string)]
    for index, value in enumerate(modes, start=1):
        output.append(f"{index}. {value}")
        menu = "\n".join(output)
    print(menu)
    if message is not None:
        print(message_compiler(message))
    mode = input(locale.SELECT_MODE).lower().strip()
    return mode
