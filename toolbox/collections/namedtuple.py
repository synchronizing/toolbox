from collections import namedtuple
from collections.abc import Mapping


def nestednamedtuple(dictionary: dict) -> namedtuple:
    """Converts dictionary to a nested namedtuple recursively.

    Args:
        dictionary: Dictionary to convert into a nested namedtuple.

    Example:

        .. code-block:: python

            from toolbox.collections.namedtuple import nestednamedtuple

            nt = nestednamedtuple({"hello": {"ola": "mundo"}})
            print(nt) # >>> namedtupled(hello=namedtupled(ola='mundo'))
    """

    if isinstance(dictionary, Mapping) and not isinstance(dictionary, fdict):
        for key, value in list(dictionary.items()):
            dictionary[key] = nestednamedtuple(value)
        return namedtuple("namedtupled", dictionary)(**dictionary)
    elif isinstance(dictionary, list):
        return [nestednamedtuple(item) for item in dictionary]

    return dictionary


class fdict(dict):
    """Forced dictionary. Prevents dictionary from becoming a nested namedtuple.

    Example:

        .. code-block:: python

            from toolbox.collections.namedtuple import nestednamedtuple, fdict

            d = {"hello": "world"}
            nt = nestednamedtuple({"forced": fdict(d), "notforced": d})
            print(nt.notforced)    # >>> namedtupled(hello='world')
            print(nt.forced)       # >>> {'hello': 'world'}
    """
