from toolbox.string.color import Format, Style, red, supports_color, strip_ansi
import pytest
import sys


class Test_color:
    class Test_Format:
        def test_format_init(self):
            Format(code=1)

        def test_format_call(self):
            formt = Format(code=1)
            assert formt("hello world").encode("utf-8") == b"\x1b[1mhello world\x1b[0m"

        def test_format_repr(self):
            formt = Format(code=1)
            assert formt.__repr__() == "Format(code=1)"

    class Test_Style:
        def test_style_init(self):
            Style(red)
            Style(1)
            Style("underline")
            Style(Format(code=31), 1, "underline")

        def test_style_init_err(self):
            with pytest.raises(TypeError):
                Style(None)

        def test_style_call(self):
            style = Style(red, 1, "underline")
            assert style("hello world") == "\x1b[31;1;4mhello world\x1b[0m"

        def test_style_repr(self):
            style = Style(red, 1, "underline")
            assert style.__repr__() == "Style(args=31;1;4)"

    class Test_supports_color:
        """ No tests are done here. This function is part of the Django test suite (hopefully)."""

    class Test_strip_ansi:
        def test_strip_ansi(self):
            assert strip_ansi(Format(code=1)("hello world")) == "hello world"
