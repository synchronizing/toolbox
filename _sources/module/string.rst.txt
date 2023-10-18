######
string
######

*****
color
*****

.. code-block:: python

    from toolbox.string import color

.. autoclass:: toolbox.string.color.Format

    Out-of-the-box this module includes the following :class:`toolbox.string.color.Format` definitions:

    .. list-table:: 
        :header-rows: 1

        *   - Foreground Color
            - Background Color
            - Styles
        *   - :py:class:`black`
            - :py:class:`bblack`
            - :py:class:`reset`
        *   - :py:class:`red`
            - :py:class:`bred`
            - :py:class:`bold`
        *   - :py:class:`green`
            - :py:class:`bgreen`
            - :py:class:`underline`
        *   - :py:class:`yellow`
            - :py:class:`byellow`
            - :py:class:`blink`
        *   - :py:class:`blue`
            - :py:class:`bblue`
            - :py:class:`reverse`
        *   - :py:class:`magenta`
            - :py:class:`bmagenta`
            - :py:class:`conceal`
        *   - :py:class:`cyan`
            - :py:class:`bcyan`
            - 
        *   - :py:class:`white`
            - :py:class:`bwhite`
            - 


    These can be utilized like so:

    .. code-block:: python

        from toolbox.string.color import bold

        print(bold("Hello world!"))

.. autoclass:: toolbox.string.color.Style

.. autofunction:: toolbox.string.color.supports_color

.. autofunction:: toolbox.string.color.strip_ansi

Module Data
===========

:py:data:`ANSI`
^^^^^^^^^^^^^^^

Dictionary with 16-bit ANSI codes.

.. code-block:: python

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

:py:data:`EC`
^^^^^^^^^^^^^

ANSI escape character that toolbox.color uses.

.. code-block:: python

    EC = "\x1B"

To modify the escape character, one may do the following:

.. code-block:: python

    from toolbox.string.color import red
    import toolbox

    toolbox.string.color.EC = "\t"

    print(red("hello world").encode("utf-8"))
    # b'\t[31mhello world\t[0m'
