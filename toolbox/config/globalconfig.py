from ..collections.namedtuple import nestednamedtuple


def make_config(**kwargs):
    """Creates a global configuration that can be accessed anywhere during runtime.

    This function is a useful replacement to passing configuration classes between classes.
    Instead of creating a `Config` object, one may use :func:`make_config` to create a
    global runtime configuration that can be accessed by any module, function, or object.

    Example:

        .. code-block:: python

            from toolbox import make_config

            make_config(hello="world")
    """

    globals()["gconf"] = kwargs


def conf():
    """Access global configuration as a nestednamedtuple.

    Example:

        .. code-block:: python

            from toolbox import conf

            print(conf().hello) # >>> 'world'
    """
    g = globals()
    if "gconf" in g:
        return nestednamedtuple(g["gconf"])
    else:
        return nestednamedtuple({})


def config():
    """Access global configuration as a dict.

    Example:

        .. code-block:: python

            from toolbox import config

            print(config()['hello']) # >>> 'world'
    """
    g = globals()
    if "gconf" in g:
        return g["gconf"]
    else:
        return {}
