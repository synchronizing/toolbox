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
        dict.__init__(
            self,
            {
                **dictionary,
                **{v: k for k, v in dictionary.items()},
                **kwargs,
                **{v: k for k, v in kwargs.items()},
            },
        )
        self.__dict__ = self


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
