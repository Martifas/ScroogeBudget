import pytest
from unittest.mock import patch, mock_open, MagicMock
from scr.menu.utilities import (
    select_separator,
    case_changer,
    message_compiler,
    menu_compiler,
)
import scr.locales.locale_en as locale


def test_select_separator():
    with patch("builtins.input", return_value="*"):
        assert select_separator() == locale.UTILITIES_SEPARATOR_SET + "*"


def test_case_changer():
    with patch("builtins.input", return_value=locale.UTILITIES_UPPERCASE):
        assert case_changer() == locale.UTILITIES_SET_TO_UPPERCASE


def test_message_compiler_uppercase():
    output_string = "hello world"
    global separator
    separator = "*"
    expected_output = f"{len(output_string) * separator}\n{output_string.upper()}\n{len(output_string) * separator}"
    assert message_compiler(output_string) == expected_output


def test_menu_compiler_no_message():
    modes = ["mode1", "mode2", "mode3"]
    output_string = "Hello World"
    expected_output = [
        f"{len(output_string)}-\n{output_string}\n{len(output_string)}-",
        "1. mode1",
        "2. mode2",
        "3. mode3",
    ]
    expected_output = "\n".join(expected_output)

    with patch(
        "scr.menu.utilities.message_compiler",
        side_effect=lambda x: f"{len(x)}-\n{x}\n{len(x)}-",
    ):
        with patch("builtins.input", return_value="1"):
            with patch("builtins.print") as mock_print:
                mode = menu_compiler(modes, output_string)
                mock_print.assert_called_with(expected_output)
                assert mode == "1"


def test_menu_compiler_with_message():
    modes = ["mode1", "mode2", "mode3"]
    output_string = "Hello World"
    message = "This is a message"
    expected_output = [
        f"{len(output_string)}-\n{output_string}\n{len(output_string)}-",
        "1. mode1",
        "2. mode2",
        "3. mode3",
    ]
    expected_output = "\n".join(expected_output)

    with patch(
        "scr.menu.utilities.message_compiler",
        side_effect=lambda x: f"{len(x)}-\n{x}\n{len(x)}-",
    ):
        with patch("builtins.input", return_value="2"):
            with patch("builtins.print") as mock_print:
                mock_print.call_args_list = []
                mode = menu_compiler(modes, output_string, message)
                assert mock_print.call_args_list[0][0][0] == expected_output
                assert (
                    mock_print.call_args_list[1][0][0]
                    == f"{len(message)}-\n{message}\n{len(message)}-"
                )
                assert mode == "2"
