from typing import Any, Optional

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

    def __init__(self, dictionary: Optional[dict] = None, **kwargs) -> dict:
        dictionary = dictionary or {}
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

    def update(self, dictionary: dict = Optional[dict], **kwargs):
        dictionary = dictionary or {}
        super(BidirectionalDict, self).update(
            {
                **dictionary,
                **{v: k for k, v in dictionary.items()},
                **kwargs,
                **{v: k for k, v in kwargs.items()},
            }
        )


class ObjectDict(BaseDict):
    """Dictionary that can be accessed and set as though it was an object.

    Example:

        .. code-block:: python

            from toolbox.collections.mapping import ObjectDict

            d = ObjectDict({"hello": "world"})
            print(d) # >>> <ObjectDict {'hello': 'world'}>

            print(d.hello) # >>> 'world'

            d.hello = "mundo"
            print(d.hello) # >>> 'mundo'
    """

    def __getattr__(self, key: Any) -> Any:
        return self.__getitem__(key)

    def __setattr__(self, key: str, value: Any):
        return self.__setitem__(key, value)


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
        if isinstance(key, bytes):
            utw = key.replace(b"_", b" ")
            wtu = key.replace(b"_", b"")
        else:
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

    def update(self, dictionary: Optional[dict] = None, **kwargs):
        err = "Cannot set key and value because this is a frozen dictionary."
        raise KeyError(err)


class MultiEntryDict(BaseDict):
    """Dictionary that can have multiple entries for the same key.

    .. code-block:: python

        from toolbox.collections.mapping import MultiEntryDict

        d = MultiEntryDict({"hello": "world", "hello": "mundo"})
        print(d) # >>> <MultiEntryDict {'hello': ['world', 'mundo']}>

        d['hello'] = 'globo'
        print(d) # >>> <MultiEntryDict {'hello': ['world', 'mundo', 'globo']}>
    """

    def __setitem__(self, key, value):
        if key in self:
            if isinstance(self[key], list):
                self[key].append(value)
            else:
                super().__setitem__(key, [self[key], value])
        else:
            super(MultiEntryDict, self).__setitem__(key, value)


class ItemDict(BaseDict):
    """Dictionary composed of :py:class:`toolbox.collections.item.Item` key and values.

    Example:

        .. code-block:: python

            from toolbox.collections.mapping import ItemDict

            d = ItemDict({"100": "one hundred"})
            print(d)
            # >>> <ItemDict {100: one hundred}>

            print(d["100"] == d[100] == d[b"100"]) # >>> True
    """

    def __init__(self, dictionary: Optional[dict] = None, **kwargs):
        dictionary = dictionary or {}
        kwargs = kwargs or {}
        dictionary = {**dictionary, **kwargs}

        new = {}
        for k, v in dictionary.items():
            if isinstance(v, list):
                new[Item(k)] = [Item(i) for i in v]
            else:
                new[Item(k)] = Item(v)

        return super(ItemDict, self).__init__(new)

    def __getitem__(self, key: ItemType):
        return super(ItemDict, self).__getitem__(Item(key))

    def __setitem__(self, key: ItemType, value: ItemType):
        if isinstance(value, list):
            super(ItemDict, self).__setitem__(Item(key), [Item(i) for i in value])
        else:
            super(ItemDict, self).__setitem__(Item(key), Item(value))

    def __delitem__(self, key: ItemType):
        super(ItemDict, self).__delitem__(Item(key))

    def __contains__(self, key: ItemType):
        return super(ItemDict, self).__contains__(Item(key))

    def update(self, dictionary: Optional[dict] = None, **kwargs):
        dictionary = dictionary or {}
        super(ItemDict, self).update(
            {
                **{Item(k): Item(v) for k, v in dictionary.items()},
                **{Item(k): Item(v) for k, v in kwargs.items()},
            },
        )
