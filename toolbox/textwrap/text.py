import textwrap


def unindent(text):
    r"""Unident triple quotes and removes any white spaces before or after text.

    Note that in the example below we are not necessarily printing the results of
    the *test* function, and instead looking at the raw string results. In real world
    situation one may expect that the \\n will not be there, and instead, line breaks will
    be in its place.

    Example:

        .. code-block:: python

            from toolbox import unident

            def test():
                return unindent(
                    '''
                    hello world
                    this is a test
                    of this functionality
                    '''
                )

            test() # >>> 'hello world\nthis is a test\nof this functionality'
    """
    return textwrap.dedent("\n".join(filter(str.strip, text.splitlines())))
