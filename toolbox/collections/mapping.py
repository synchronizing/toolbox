from typing import Any

from .item import Item, ItemType


class BaseDict(dict):
    """Dictionary with pretty :py:func:`__repr__` output.

    Base class that all other dictionaries in this file inherit from. :py:func:`__repr__` is
    replaced with ``<{class_name} {dictionary data}>`` output style for implicit inferences.

    Example:

        .. code-block:: python

            from toolbox.collections.mapping import BaseDict

            class NewDict(BaseDict):
                '''New dictionary example.'''

            d = NewDict({"hello": "world"})
            print(d) # >>> <NewDict {'hello': 'world'}>
    """

    def __repr__(self):
        return "<{} {}>".format(
            self.__class__.__name__,
            super(BaseDict, self).__repr__(),
        )


class BidirectionalDict(BaseDict):
    """Dictionary with two-way capabilities.

    Example:

        .. code-block:: python

            from toolbox.collections.mapping import BidirectionalDict

            d = BidirectionalDict({"hello": "world"})
            print(d) # >>> <BidirectionalDict {'hello': 'world', 'world': 'hello'}>
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

    def update(self, dictionary: dict = {}, **kwargs):
        super(BidirectionalDict, self).update(
            {
                **dictionary,
                **{v: k for k, v in dictionary.items()},
                **kwargs,
                **{v: k for k, v in kwargs.items()},
            }
        )


class ObjectDict(BaseDict):
    """Dictionary that can be accessed as though it was an object.

    Example:

        .. code-block:: python

            from toolbox.collections.mapping import ObjectDict

            d = ObjectDict({"hello": "world"})
            print(d) # >>> <ObjectDict {'hello': 'world'}>

            print(d.hello) # >>> 'world'
    """

    def __getattr__(self, key: Any) -> Any:
        return self.__getitem__(key)


class OverloadedDict(BaseDict):
    """Dictionary that can be added or subtracted.

    Example:

        .. code-block:: python

            from toolbox.collections.mapping import OverloadedDict

            d1 = OverloadedDict({"hello": "world"})
            d2 = {"ola": "mundo"}

            d1 += d2
            print(d1) # >>> <OverloadedDict {'hello': 'world', 'ola': 'mundo'}>

            d1 -= d2
            print(d1) # >>> <OverloadedDict {'hello': 'world'}>
    """

    def __add__(self, other: dict) -> dict:
        dct = {**self, **other}
        return OverloadedDict(dct)

    def __iadd__(self, other: dict) -> dict:
        self = self.__add__(other)
        return self

    def __sub__(self, other: dict) -> dict:
        dct = {k: v for k, v in self.items() if (k, v) not in other.items()}
        return OverloadedDict(dct)

    def __isub__(self, other: dict) -> dict:
        self = self.__sub__(other)
        return self


class UnderscoreAccessDict(BaseDict):
    """Dictionary that doesn't distinct keys with empty spaces and underscores.

    Example:

        .. code-block:: python

            from toolbox.collections.mapping import UnderscoreAccessDict

            d = UnderscoreAccessDict({"hello world": "ola mundo"})
            print(d) # >>> <UnderscoreAccessDict {'hello world': 'ola mundo'}>

            print(d['hello_world']) # >>> 'ola mundo'
    """

    def __getitem__(self, key: Any) -> Any:
        utw = key.replace("_", " ")
        wtu = key.replace("_", "")
        if utw in self:
            return super(UnderscoreAccessDict, self).__getitem__(utw)
        elif wtu in self:
            return super(UnderscoreAccessDict, self).__getitem__(wtu)

        return super(UnderscoreAccessDict, self).__getitem__(key)


class FrozenDict(BaseDict):
    """Dictionary that is frozen.

    .. code-block:: python

        from toolbox.collections.mapping import FrozenDict

        d = FrozenDict({"hello": "world"})
        print(d) # >>> <FrozenDict {'hello': 'world'}>

        d['ola'] = 'mundo'
        # >>> KeyError: 'Cannot set key and value because this is a frozen dictionary.'
    """

    def __setitem__(self, key, value):
        err = "Cannot set key and value because this is a frozen dictionary."
        raise KeyError(err)

    def update(self, dictionary: dict = {}, **kwargs):
        err = "Cannot set key and value because this is a frozen dictionary."
        raise KeyError(err)


class ItemDict(BaseDict):
    """Dictionary composed of :py:class:`toolbox.collections.item.Item` key and values.

    Example:

        .. code-block:: python

            from toolbox.collections.mapping import ItemDict

            d = ItemDict({"100": "one hundred"})
            print(d)
            # >>> <ItemDict {Item(bytes=b'100', str='100', int=100, bool=True, original_type=str): Item(bytes=b'one hundred', str='one hundred', int=None, bool=True, original_type=str)}>

            print(d["100"] == d[100] == d[b"100"]) # >>> True
    """

    def __init__(self, dictionary: dict = {}, **kwargs):
        super(ItemDict, self).__init__(
            {
                **{Item(k): Item(v) for k, v in dictionary.items()},
                **{Item(k): Item(v) for k, v in kwargs.items()},
            }
        )

    def __getitem__(self, key: ItemType):
        return super(ItemDict, self).__getitem__(Item(key))

    def __setitem__(self, key: ItemType, value: ItemType):
        super(ItemDict, self).__setitem__(Item(key), Item(value))

    def __delitem__(self, key: ItemType):
        super(ItemDict, self).__delitem__(Item(key))

    def __contains__(self, key: ItemType):
        return super(ItemDict, self).__contains__(Item(key))

    def update(self, dictionary: dict = {}, **kwargs):
        super(ItemDict, self).update(
            {
                **{Item(k): Item(v) for k, v in dictionary.items()},
                **{Item(k): Item(v) for k, v in kwargs.items()},
            },
        )
