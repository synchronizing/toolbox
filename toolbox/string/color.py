import os
import re
import sys
from typing import Optional, Tuple, Union

# Dictionary with 16-bit ANSI codes.
ANSI = {
    # Foreground Colors
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37",
    # Background Colors
    "bblack": "40",
    "bred": "41",
    "bgreen": "42",
    "byellow": "43",
    "bblue": "44",
    "bmagenta": "45",
    "bcyan": "46",
    "bwhite": "47",
    # Styles
    "reset": "0",
    "bold": "1",
    "underline": "4",
    "blink": "5",
    "reverse": "7",
    "conceal": "8",
}

# ANSI escape character that toolbox.string.color uses.
EC = "\x1B"


class Format:
    def __init__(self, code: int):
        r"""Creates a new ANSI format that can be called to retrieve a styled string.

        Args:
            code: ANSI code.

        Example:

        .. code-block:: python

            from toolbox.string.color import Format

            bold = Format(code="1")
            print(bold("hello world"))
        """
        self.code = code

    def __call__(self, string: str, reset: bool = True):
        """Returns a string with ANSI code.

        Args:
            string: String to stylize.
            reset: Optional flag to append reset ANSI code on specific call.
        """

        fin = "{}[{}m{}".format(EC, self.code, string)
        if reset:
            fin += "{}[{}m".format(EC, ANSI["reset"])

        return fin

    def __repr__(self):
        return "Format(code={})".format(self.code)


class Style:
    def __init__(self, *args: Tuple[Union[str, int, "Format"]], reset: bool = True):
        """Initializes a complex ANSI style that can be called to retrieve a styled string.

        Args:
            args: Arguments that can be either a string, integer, or Format type to create a
                new ANSI style.
            reset: Boolean flag that when set to True will append the ANSI reset code to ensure
                no style spill over.

        Note:
            :py:class:`Style` can take arguments of type string, int, and Format. When
            using string, it will look up the ANSI code in the 16-bit ANSI dictionary.
            To use a non-standard code use either a custom Format, or an integer representation
            of the ANSI code.

        Example:

        .. code-block:: python

            from toolbox.string.color import Style, red

            # ANSI code 1 is bold.
            error = Style(red, 1, "underline")
            print(error("This is an error"))
        """

        if not all(isinstance(x, (int, str, Format)) for x in args):
            err = "Arguments must either be of format 'Format', 'int', or 'str'."
            raise TypeError(err)

        self.args = args
        self.reset = reset

    def __call__(self, text: str, reset: Optional[bool] = None):
        """Returns a string with ANSI codes set.

        Args:
            string: String to stylize.
            reset: Optional flag to append reset ANSI code on specific call.
        """

        codes = self._args_codes()
        reset = reset if reset else self.reset
        return Format(code=";".join(codes))(text, reset=reset)

    def _args_codes(self):
        codes = []
        for arg in self.args:
            if isinstance(arg, int):
                codes.append(str(arg))
            elif isinstance(arg, str):
                codes.append(ANSI[arg])
            elif isinstance(arg, Format):
                codes.append(str(arg.code))

        return codes

    def __repr__(self):
        return "Style(args={})".format(";".join(self._args_codes()))


black = Format(code=30)
red = Format(code=31)
green = Format(code=32)
yellow = Format(code=33)
blue = Format(code=34)
magenta = Format(code=35)
cyan = Format(code=36)
white = Format(code=37)
bblack = Format(code=40)
bred = Format(code=41)
bgreen = Format(code=42)
byellow = Format(code=43)
bblue = Format(code=44)
bmagenta = Format(code=45)
bcyan = Format(code=46)
bwhite = Format(code=47)
reset = Format(code=0)
bold = Format(code=1)
underline = Format(code=4)
blink = Format(code=5)
reverse = Format(code=7)
conceal = Format(code=8)


def supports_color() -> bool:  # pragma: no cover
    """Checks if system's terminal has color support.

    Note:
        This piece of code is from Django's source code
        `here <https://github.com/django/django/blob/b41d38ae26b1da9519a6cd765bc2f2ce7d355007/django/core/management/color.py#L20-L56>`_.

        Copyright (c) Django Software Foundation and individual contributors.
    """

    try:
        import colorama
    except ImportError:
        HAS_COLORAMA = False
    else:
        colorama.init()
        HAS_COLORAMA = True

    def vt_codes_enabled_in_windows_registry():
        """ Check the Windows Registry to see if VT code handling has been enabled by default, see https://superuser.com/a/1300251/447564."""

        try:
            # winreg is only available on Windows.
            import winreg
        except ImportError:
            return False
        else:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Console")
            try:
                reg_key_value, _ = winreg.QueryValueEx(reg_key, "VirtualTerminalLevel")
            except FileNotFoundError:
                return False
            else:
                return reg_key_value == 1

    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

    return is_a_tty and (
        sys.platform != "win32"
        or HAS_COLORAMA
        or "ANSICON" in os.environ
        or
        # Windows Terminal supports VT codes.
        "WT_SESSION" in os.environ
        or
        # Microsoft Visual Studio Code's built-in terminal supports colors.
        os.environ.get("TERM_PROGRAM") == "vscode"
        or vt_codes_enabled_in_windows_registry()
    )


def strip_ansi(text: str) -> str:
    """Removes ANSI color/style sequence.

    Args:
        text: String to remove ANSI style from.

    Example:

        .. code-block:: python

            from toolbox import strip_ansi, red

            print(strip_ansi(red("hello world")))
    """

    return re.sub(r"\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?", "", text)
