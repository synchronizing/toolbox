from inspect import currentframe, getframeinfo


def sprinkle(*args):
    """
    Prints the line and file that this function was just called from.

    Example:

        .. code-block:: python

            from toolbox.pdb.sprinkle import sprinkle
            sprinkle() # >>> 13 sprinke.py
            sprinkle("hello", "world") # >>> 14 sprinke.py hello world
    """

    frameinfo = getframeinfo(currentframe().f_back)
    print(frameinfo.lineno, frameinfo.filename, *args)
