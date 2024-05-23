from scr.menu.utilities import menu_compiler
import scr.locales.locale_en as locale
from scr.menu.username import read_profile_file
import numpy as np
import datetime
import re

def forecast_menu(username):
    modes = locale.FORECAST_MODES
    title = locale.FORECAST_TITLE
    mode = menu_compiler(modes, title)
    match mode:
        case _ if mode in locale.FORECAST_SELECT_MODE_1:
            message = forecast_date(username)
        case _ if mode in locale.FORECAST_SELECT_MODE_2:
            message = forecast_amount(username)
    return message


def forecast_date(username):
    savings_monthly_average, existing_savings = get_savings_data(username)
    if savings_monthly_average is None or existing_savings is None:
        message = locale.FORECAST_ERROR_NO_DATA
        return message

    wanted_amount = int(input(locale.FORECAST_AMOUNT_WANTED))
    if wanted_amount <= existing_savings:
        message = f"{locale.FORECAST_ALREADY_HAVE}{existing_savings}"
        return message

    months_needed = int((wanted_amount - existing_savings) / savings_monthly_average)
    current_date = datetime.date.today()
    forecasted_date = current_date + datetime.timedelta(days=months_needed*30)
    message = (f"{locale.FORECAST_DATE_BASED}{savings_monthly_average:.0f}, "
               f"{locale.FORECAST_REACH_GOAL}{wanted_amount} {locale.FORECAST_IN} {months_needed} {locale.FORECAST_MONTHS}, "
               f"{locale.FORECAST_APPROXIMATELY}{forecasted_date.strftime(locale.YEAR_MONTH)}.")
    return message

def forecast_amount(username):
    savings_monthly_average, existing_savings = get_savings_data(username)
    if savings_monthly_average is None or existing_savings is None:
        message = locale.FORECAST_ERROR_NO_DATA
        return message

    while True:
        target_date_str = input(locale.FORECAST_DATE_WANTED)
        if not re.match(r"^\d{4}-\d{2}$", target_date_str):
            message = locale.FORECAST_INVALID_FORMAT
            continue
        target_date = datetime.datetime.strptime(target_date_str, locale.YEAR_MONTH)
        current_date = datetime.date.today()
        if target_date.date() < current_date:
            print(locale.FORECAST_NO_LOWER_DATE)
            continue
        break

    months_diff = (target_date.year - current_date.year) * 12 + (target_date.month - current_date.month)
    forecasted_amount = existing_savings + (savings_monthly_average * months_diff)
    
    message = (f"{locale.FORECAST_DATE_BASED}{savings_monthly_average:.0f}, "
               f"{locale.FORECAST_SAVINGS}{target_date_str} {locale.FORECAST_IS_APPROXIMATELY} {forecasted_amount:.0f}.")
    return message
    
def get_savings_data(username):
    transactions_data = read_profile_file(username, transactions=True)[0]
    if not transactions_data:
        return None, None
    
    savings_data = [int(row[2]) for row in transactions_data if row[0] == "savings"]
    if not savings_data: 
        return None, None
    
    savings_monthly_average = np.mean(savings_data)
    existing_savings = int(read_profile_file(username)[0][1][1])
    return savings_monthly_average, existing_savings