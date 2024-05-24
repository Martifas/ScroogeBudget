import sys
import scr.locales.locale_en as locale
from scr.menu.menu import menu_handling


def main() -> None:
    """
    The main entry point of the ScroogeBudget application.
    It calls the menu_handling function to start the application.
    If an EOFError occurs, it exits the program with the MAIN_EXIT message.
    """

    try:
        menu_handling()
    except EOFError:
        sys.exit(locale.MAIN_EXIT)


if __name__ == "__main__":
    main()
