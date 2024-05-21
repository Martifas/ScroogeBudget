import scr.locales.locale_en as locale
from scr.menu.utilities import menu_compiler, select_separator, case_changer
from scr.menu.balance import Balance
from scr.menu.username import profile_option


balance = None
username = None

def menu_handling(message: str = None, username: str = None) -> None:
    modes = locale.MENU_HANDLING_MODES
    while True:
        mode = menu(message)
        if mode not in modes:
            message = locale.ERROR_WRONG_INPUT
            continue
        if username is None and mode not in locale.MENU_HANDLING_MODES_WITHOUT_PROFILE :
            message = locale.MENU_HANDLING_USER
            continue
        mode_select(mode, username)
        break

def menu(message: str = None) -> str:
    modes = locale.MENU_MODES
    title = locale.MENU_TITLE
    mode = menu_compiler(modes, title, message)
    return mode

def mode_select(mode: str, username: str = None) -> None:
    global balance
    match mode:
        case _ if mode in locale.MODE_SELECT_BALANCE_1 :
            if not Balance(username).balance_menu():
                menu_handling(username=username)
        case _ if mode in locale.MODE_SELECT_FORECAST_2 :
            print("TESTAS 2")
            #print("Forecast running")
        case _ if mode in locale.MODE_SELECT_STATISTICS_3 :
            print("TESTAS 3")
            #stats_menu()
        case _ if mode in locale.MODE_SELECT_PROFILE_4 :
            balance, message, username = profile_option()
            menu_handling(message=message, username=username)
        case _ if mode in locale.MODE_SELECT_OPTIONS_5:
            print("TESTAS 5")
            message = options()
            menu_handling(message=message)
        case _ if mode in locale.MODE_SELECT_EXIT_6 :
            print("TESTAS 6")
            raise EOFError


def options():
    modes = locale.OPTIONS_MODES
    title = locale.OPTIONS_TITLE
    mode = menu_compiler(modes, title)
    if mode == "1":
        message = select_separator()
    elif mode == "2":
        case = case_changer()
        message = locale.OPTIONS_MESSAGE + case
    else:
        message = locale.OPTIONS_ERROR
    return message
