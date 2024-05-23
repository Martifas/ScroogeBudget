import scr.locales.locale_en as locale
from scr.menu.utilities import menu_compiler, select_separator, case_changer
from scr.menu.balance import Balance
from scr.menu.username import profile_option
from scr.menu.stats import Stats

balance = None
username = None


def menu_handling(message: str = None, username: str = None) -> None:
    modes = locale.MENU_HANDLING_MODES

    while True:
        mode = menu(message)

        if mode not in modes:
            message = locale.ERROR_WRONG_INPUT
            continue

        if username is None and mode not in locale.MENU_HANDLING_MODES_WITHOUT_PROFILE:
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
        case _ if mode in locale.MODE_SELECT_BALANCE_1:
            if not Balance(username).balance_menu():
                menu_handling(username=username)
        case _ if mode in locale.MODE_SELECT_STATISTICS_2:
            username = Stats(username).stats_menu(username)
            menu_handling(username=username)
        case _ if mode in locale.MODE_SELECT_PROFILE_3:
            balance, message, username = profile_option()
            menu_handling(message=message, username=username)
        case _ if mode in locale.MODE_SELECT_OPTIONS_4:
            message = options(username)
            menu_handling(message=message)
        case _ if mode in locale.MODE_SELECT_EXIT_5:
            raise EOFError


def options(username) -> str:
    modes = locale.OPTIONS_MODES
    title = locale.OPTIONS_TITLE
    mode = menu_compiler(modes, title)

    options_actions = {"1": select_separator, "2": case_changer}

    if mode in options_actions:
        message = options_actions[mode]()
    else:
        message = locale.OPTIONS_ERROR

    menu_handling(message,username)
