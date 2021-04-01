import importlib
import pkg_resources


def search_package(pkg: str, method: str = "is", imports: bool = False) -> dict:
    """Discover packages installed in the system.

    Function iterates through all of the installed packages in the system and returns a dictionary
    with all modules that passes the search criteria passed by ``method``.

    Args:
        pkg: Package name to search for.
        method: String that is either ``is``, ``in``, or ``startswith``.
        imports: Boolean that indicates whether or not to import the found package(s).

    Raises:
        TypeError: The search method passed is invalid.

    Note:
        The search method must be one of the following:

        * ``is``: Returns modules that are exactly worded ``pkg``.
        * ``in``: Returns modules that contains the string ``pkg``.
        * ``startswith``: Return modules that starts with the passed ``pkg`` name.

        When ``imports`` is set to ``False`` this function returns a
        ``Dict[str, str]`` where the key is the name of the module, and
        the value is the version installed on the system.

        If ``imports`` is set to ``True`` this function returns a
        ``Dict[str, Module]`` where the key is the name of the module,
        and the value is the _imported_ module.

    Example:

        .. code-block:: python

            from toolbox.pkgutil.package import search_package

            print(search_package("toolbox", method="is"))
            # >>> {'toolbox': '1.4.0'}

            print(search_package("toolbox", method="is", imports=True))
            # >>> {'toolbox': <module 'toolbox' from '.../toolbox/toolbox/__init__.py'>}

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

    installed_pkgs = {
        pkg.project_name: pkg.version for pkg in pkg_resources.working_set
    }

    packages = {}
    for package, version in installed_pkgs.items():
        if search(package):
            if imports:
                packages[package] = importlib.import_module(package)
            else:
                packages[package] = version

    return packages
