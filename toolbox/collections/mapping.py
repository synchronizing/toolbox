from typing import Any


class BidirectionalDict(dict):
    """Dictionary with two-way capabilities.

    Example:

        .. code-block:: python

            from toolbox.collections.mapping import BidirectionalDict

            d = BidirectionalDict({"hello": "world"})
            print(d) # >>> {'hello': 'world', 'world': 'hello'}
    """

    def __init__(self, dictionary: dict = {}, **kwargs) -> dict:
        super(BidirectionalDict, self).__init__(
            {
                **dictionary,
                **{v: k for k, v in dictionary.items()},
                **kwargs,
                **{v: k for k, v in kwargs.items()},
            }
        )

    def __setitem__(self, key: Any, value: Any):
        super(BidirectionalDict, self).__setitem__(key, value)
        super(BidirectionalDict, self).__setitem__(value, key)


class ObjectDict(dict):
    """Dictionary that can be accessed as though it was an object.

    Example:

        .. code-block:: python

            from toolbox.collections.mapping import ObjectDict

            d = ObjectDict({"hello": "world"})
            print(d.hello) # >>> 'world'
    """

    def __getattr__(self, key: Any) -> Any:
        return self.__getitem__(key)


class OverloadedDict(dict):
    """Dictionary that can be added or subtracted.

    Example:

        .. code-block:: python

            from toolbox.collections.mapping import OverloadedDict

            d1 = OverloadedDict({"hello": "world"})
            d2 = OverloadedDict({"ola": "mundo"})
            d1 += d2
            print(d1) # >>> {'hello': 'world', 'ola': 'mundo'}
            d1 -= d2
            print(d1) # >>> {'hello': 'world'}
    """

    def __add__(self, other: dict) -> dict:
        d = {**self, **other}
        return OverloadedDict(d)

    def __iadd__(self, other: dict) -> dict:
        self = self.__add__(other)
        return self

    def __sub__(self, other: dict) -> dict:
        d = {k: v for k, v in self.items() if (k, v) not in other.items()}
        return OverloadedDict(d)

    def __isub__(self, other: dict) -> dict:
        self = self.__sub__(other)
        return self


class UnderscoreAccessDict(dict):
    """Dictionary that doesn't distinct keys with empty spaces and underscores.

    Example:

        .. code-block:: python

            from toolbox.collections.mapping import UnderscoreAccessDict

            d = UnderscoreAccessDict({"hello world": "ola mundo"})
            d['hello_world'] # >>> 'ola mundo'
    """

    def __getitem__(self, key: Any) -> Any:
        utw = key.replace("_", " ")
        wtu = key.replace("_", "")
        if utw in self:
            return super(UnderscoreAccessDict, self).__getitem__(utw)
        elif wtu in self:
            return super(UnderscoreAccessDict, self).__getitem__(wtu)

        return super(UnderscoreAccessDict, self).__getitem__(key)
