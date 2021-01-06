from collections import namedtuple

from ..collections.namedtuple import nestednamedtuple


def make_config(dictionary: dict = {}, **kwargs) -> None:
    """Creates a global configuration that can be accessed anywhere during runtime.

    This function is a useful replacement to passing configuration classes between classes.
    Instead of creating a `Config` object, one may use :func:`make_config` to create a
    global runtime configuration that can be accessed by any module, function, or object.

    Args:
        dictionary: Dictionary to create global configuration with.
        kwargs: Arguments to make global configuration with.

    Example:

        .. code-block:: python

            from toolbox.config.globalconfig import make_config

            make_config(hello="world")
    """

    globals()["gconf"] = {**dictionary, **kwargs}


def conf() -> namedtuple:
    """Access global configuration as a :class:`toolbox.collections.namedtuple.nestednamedtuple`.

    Example:

        .. code-block:: python

            from toolbox.config.globalconfig import conf

            print(conf().hello) # >>> 'world'
    """
    g = globals()
    if "gconf" in g:
        return nestednamedtuple(g["gconf"])
    else:
        return nestednamedtuple({})


def config() -> dict:
    """Access global configuration as a dict.

    Example:

        .. code-block:: python

            from toolbox.config.globalconfig import config

            print(config()['hello']) # >>> 'world'
    """
    g = globals()
    if "gconf" in g:
        return g["gconf"]
    else:
        return {}
