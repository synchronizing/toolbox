from typing import Union, Iterator

ENCODE = "ascii"
ItemType = Union[bytes, str, int, bool, None, "Item"]


class Item:
    __slots__ = ["_item", "_type"]

    def __init__(self, item: ItemType):
        """An interface for type-agnostic operations between ``bytes``, ``str``, ``int``, ``bool``,
        and ``None``.

        Internally, the passed ``item`` object is stored as its ``bytes`` representation. Any
        operation or modification to the new ``Item`` instance is done to the internal ``bytes``
        object. The true usefulness of this container is for type-agnostic operations such as
        equality checks.
        
        Args:
            item: Input to be stored.

        Example:

            .. code-block:: python

                from toolbox.collections.item import Item

                item = Item("hello world")
                if b" world" in item:
                    item -= " world"

                print(item.raw, item.string)
                # >>> b'hello' hello

                print(repr(item))
                # >>> Item(bytes=b'hello', str='hello', int=None, bool=True, original_type=str)
        """
        self._type = type(item)
        self._item = self.byte_item(item=item)

    @property
    def raw(self) -> bytes:
        """Bytes representation of the passed item."""
        return self._item

    @property
    def string(self) -> str:
        """String representation of the passed item."""
        return self._item.decode(ENCODE)

    @property
    def integer(self) -> Union[int, None]:
        """Integer representation of the passed item.

        If passed item is not a sub class of type int or str.isdigit() this property returns None.
        """
        if issubclass(self._type, int) or self.string.isdigit():
            return int(self._item)
        else:
            return None

    @property
    def boolean(self) -> bool:
        """Boolean representation of the passed item."""
        if issubclass(self._type, int):
            return bool(int(self._item))
        else:
            return bool(self._item)

    @property
    def original(self) -> ItemType:
        """Original representation of the passed item."""
        if self._type is str and isinstance(self._item, bytes):
            return self._item.decode(ENCODE)
        elif self._type is type(None):
            return None

        return self._type(self._item)

    def replace(self, old: ItemType, new: ItemType, count: int = -1) -> bytes:
        """``bytes.replace()`` functionality on item.

        See Python `docs <https://docs.python.org/3/library/stdtypes.html?highlight=replace#bytes.replace>`_ for more info.
        """
        old = self.byte_item(item=old)
        new = self.byte_item(item=new)
        return self.raw.replace(old, new, count)

    def __pos__(self):
        """Returns the string representation of the object.

        Example:

            .. code-block:: python

                from toolbox.collections.item import Item

                item = Item(100)
                print(+item, type(+item)) # >>> 100 <class 'str'>
        """
        return self.string

    def __neg__(self):
        """Returns the integer representation of the object.

        Example:

            .. code-block:: python

                from toolbox.collections.item import Item

                item = Item(100)
                print(-item, type(-item)) # >>> 100 <class 'int'>
        """
        return self.integer

    def __contains__(self, item: ItemType) -> bool:
        _item = self.byte_item(item=item)
        return _item in self._item

    def __eq__(self, item: ItemType) -> bool:
        _item = self.byte_item(item=item)
        return self._item == _item

    def __add__(self, item: ItemType) -> "Item":
        _item = self.byte_item(item=item)
        return Item(self._item + _item)

    def __iadd__(self, item: ItemType) -> "Item":
        self._item = (self + Item(item))._item
        return self

    def __sub__(self, item: ItemType) -> "Item":
        _item = self.byte_item(item=item)
        return Item(self._item.replace(_item, b""))

    def __isub__(self, item: ItemType) -> "Item":
        self._item = (self - Item(item))._item
        return self

    def __iter__(self) -> Iterator[str]:
        return iter(self.string)

    def __hash__(self) -> int:
        return hash(self._item)

    def __len__(self) -> int:
        return len(self.raw)

    def __bool__(self) -> bool:
        return self.boolean

    def __str__(self) -> str:
        return self.string

    def __repr__(self) -> str:
        return "Item(bytes={}, str='{}', int={}, bool={}, original_type={})".format(
            self.raw,
            self.string,
            self.integer,
            self.boolean,
            self._type.__name__,
        )

    @staticmethod
    def byte_item(item: ItemType) -> "Item":
        """Converts passed item into its bytes representation, and returns an Item instance.

        Args:
            item: Item of str, bytes, int, bool, None, or Item to convert to an Item.
        """

        if isinstance(item, str):
            _item = item.encode(ENCODE)
        elif isinstance(item, bytes):
            _item = item
        elif isinstance(item, int):
            _item = b"%d" % item
        elif item is None:
            _item = b""
        elif isinstance(item, Item):
            _item = item.raw
        else:
            err = "Passed 'item' is not of type str, bytes, int, None, or Item."
            raise TypeError(err)

        return _item
