import importlib
import pkgutil


def search_package(pkg: str, method: str = "is") -> dict:
    """Discover packages installed in the system.

    Function iterates through all of the installed packages in the system and returns a dictionary
    with all modules that passes the search criteria passed by ``method``.

    Args:
        pkg: Package name to search for.
        method: String that is either ``is``, ``in``, or ``startswith``.

    Raises:
        TypeError: The search method passed is invalid.

    Note:
        The search method must be one of the following:

        * ``is``: Returns modules that are exactly worded ``pkg``.
        * ``in``: Returns modules that contains the string ``pkg``.
        * ``startswith``: Return modules that starts with the passed ``pkg`` name.

    Example:

        .. code-block:: python

            from toolbox.pkgutil.package import search_package

            print(search_package("toolbox", method="is"))
            # >>> {'toolbox': <module 'toolbox' from '.../toolbox/__init__.py'>}
    """

    if method == "is":
        search = lambda name: name == pkg
    elif method == "in":
        search = lambda name: pkg in name
    elif method == "startswith":
        search = lambda name: name.startswith(pkg)
    else:
        err = "Search method must be either 'is', 'in', or 'startswith'."
        raise TypeError(err)

    packages = {}
    for _, name, ispkg in pkgutil.iter_modules():
        if ispkg and search(name):
            packages[name] = importlib.import_module(name)

    return packages
