from scr.menu.utilities import menu_compiler
import scr.locales.locale_en as locale
from scr.menu.username import read_profile_file
import numpy as np
import datetime
import re


def forecast_menu(username: str, message: str = None) -> str:
    while True:
        modes = locale.FORECAST_MODES
        title = locale.FORECAST_TITLE
        mode = menu_compiler(modes, title, message)
        if mode == locale.BACK:
            return None
        match mode:
            case _ if mode in locale.FORECAST_SELECT_MODE_1:
                result = forecast_date(username)
            case _ if mode in locale.FORECAST_SELECT_MODE_2:
                result = forecast_amount(username)
            case _:
                result = locale.ERROR_WRONG_INPUT
        if result == locale.BACK:
            continue
        else:
            return result


def forecast_date(username: str) -> str:
    """
    Forecast the date when the user will reach their desired savings amount.

    Args:
        username (str): The username of the user.

    Returns:
        str: A message indicating the forecasted date or an error message.
    """
    savings_monthly_average, existing_savings = real_or_custom(username)
    if savings_monthly_average is None or existing_savings is None:
        message = locale.FORECAST_ERROR_NO_DATA
        return message
    while True:
        wanted_amount = input(locale.FORECAST_AMOUNT_WANTED).strip()
        if wanted_amount.lower() == locale.BACK:
            return locale.BACK
        try:
            wanted_amount = int(wanted_amount)
            break
        except ValueError:
            print(locale.ERROR_WRONG_INPUT)
    if wanted_amount <= existing_savings:
        message = f"{locale.FORECAST_ALREADY_HAVE}{existing_savings}"
        return message
    months_needed = int((wanted_amount - existing_savings) / savings_monthly_average)
    current_date = datetime.date.today()
    forecasted_date = current_date + datetime.timedelta(days=months_needed * 30)
    message = (
        f"{locale.FORECAST_DATE_BASED}{savings_monthly_average:.0f}, "
        f"{locale.FORECAST_REACH_GOAL}{wanted_amount} {locale.FORECAST_IN} {months_needed} {locale.FORECAST_MONTHS}, "
        f"{locale.FORECAST_APPROXIMATELY}{forecasted_date.strftime(locale.YEAR_MONTH)}."
    )
    return message


def forecast_amount(username: str) -> str:
    """
    Forecast the savings amount on a specific target date.

    Args:
        username (str): The username of the user.

    Returns:
        str: A message indicating the forecasted savings amount or an error message.
    """
    savings_monthly_average, existing_savings = real_or_custom(username)
    if savings_monthly_average is None or existing_savings is None:
        message = locale.FORECAST_ERROR_NO_DATA
        return message
    while True:
        target_date_str = input(locale.FORECAST_DATE_WANTED).strip()
        if target_date_str.lower() == locale.BACK:
            return locale.BACK
        if not re.match(r"^\d{4}-\d{2}$", target_date_str):
            message = locale.FORECAST_INVALID_FORMAT
            continue
        target_date = datetime.datetime.strptime(target_date_str, locale.YEAR_MONTH)
        current_date = datetime.date.today()
        if target_date.date() < current_date:
            print(locale.FORECAST_NO_LOWER_DATE)
            continue
        break
    months_diff = (target_date.year - current_date.year) * 12 + (
        target_date.month - current_date.month
    )
    forecasted_amount = existing_savings + (savings_monthly_average * months_diff)
    message = (
        f"{locale.FORECAST_DATE_BASED}{savings_monthly_average:.0f}, "
        f"{locale.FORECAST_SAVINGS}{target_date_str} {locale.FORECAST_IS_APPROXIMATELY} {forecasted_amount:.0f}."
    )
    return message


def get_savings_data(username: str) -> tuple:
    """
    Retrieve the user's savings data from their transactions file.

    Args:
        username (str): The username of the user.

    Returns:
        tuple: A tuple containing the average monthly savings and the existing savings amount,
               or (None, None) if no savings data is found.
    """
    transactions_data = read_profile_file(username, transactions=True)[0]
    if not transactions_data:
        return None, None
    savings_data = [int(row[2]) for row in transactions_data if row[0] == "savings"]
    if not savings_data:
        return None, None
    savings_monthly_average = np.mean(savings_data)
    existing_savings = int(read_profile_file(username)[0][1][1])
    return savings_monthly_average, existing_savings


def real_or_custom(username: str) -> int:
    """
    Prompt the user to choose between using real savings data or entering custom data for forecasting.

    Args:
        username (str): The username of the user.

    Returns:
        int: A tuple containing the average monthly savings and the existing savings amount.
    """
    while True:
        real_custom = input(locale.FORECAST_REAL_CUSTOM).strip().lower()
        if real_custom == "1":
            savings_monthly_average, existing_savings = get_savings_data(username)
        elif real_custom == "2":
            savings_monthly_average = int(input(locale.FORECAST_SAVINGS_EVERY_MONTH))
            existing_savings = int(input(locale.FORECAST_SAVINGS_NOW))
        else:
            print(locale.ERROR_WRONG_INPUT)
            continue
        return savings_monthly_average, existing_savings
