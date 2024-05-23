import sys
import scr.locales.locale_en as locale
from scr.menu.menu import menu_handling


def main() -> None:
    try:
        menu_handling()
    except EOFError:
        sys.exit(locale.MAIN_EXIT)


if __name__ == "__main__":
    main()
