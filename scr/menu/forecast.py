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
            forecast_date(username)
        case _ if mode in locale.FORECAST_SELECT_MODE_2:
            forecast_amount(username)

def get_savings_data(username):
    transactions_data = read_profile_file(username, transactions=True)[0]
    if not transactions_data:
        print("Data missing for forecast")
        return None, None
    
    savings_data = [int(row[2]) for row in transactions_data if row[0] == "savings"]
    if not savings_data:
        print("Data missing for forecast")
        return None, None
    
    savings_monthly_average = np.mean(savings_data)
    existing_savings = int(read_profile_file(username)[0][1][1])
    return savings_monthly_average, existing_savings

def forecast_date(username):
    savings_monthly_average, existing_savings = get_savings_data(username)
    if savings_monthly_average is None or existing_savings is None:
        return
    
    wanted_amount = int(input("What amount of savings would you like to have? "))
    months_needed = int((wanted_amount - existing_savings) / savings_monthly_average)
    current_date = datetime.date.today()
    forecasted_date = current_date + datetime.timedelta(days=months_needed*30)
    print(f"Based on your average monthly savings of {savings_monthly_average:.2f}, "
          f"\nYou will reach your savings goal of {wanted_amount} in {months_needed} months, "
          f"\nWhich is approximately {forecasted_date.strftime(locale.YEAR_MONTH)}.")

def forecast_amount(username):
    savings_monthly_average, existing_savings = get_savings_data(username)
    if savings_monthly_average is None or existing_savings is None:
        return
    
    while True:
        target_date_str = input("Enter the target date (YYYY-MM): ")
        if not re.match(r"^\d{4}-\d{2}$", target_date_str):
            print("Invalid date format. Please enter the date in the format YYYY-MM.")
            continue
        
        target_date = datetime.datetime.strptime(target_date_str, locale.YEAR_MONTH)
        current_date = datetime.date.today()
        if target_date.date() < current_date:
            print("Target date cannot be lower than today's date.")
            continue
        
        break
    
    months_diff = (target_date.year - current_date.year) * 12 + (target_date.month - current_date.month)
    forecasted_amount = existing_savings + (savings_monthly_average * months_diff)
    print(f"Based on your average monthly savings of {savings_monthly_average:.2f}, "
          f"your forecasted savings amount on {target_date_str} is approximately {forecasted_amount:.2f}.")