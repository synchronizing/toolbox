###########
collections
###########

****
item
****

.. code-block:: python

    from toolbox.collections import item

.. autoclass:: toolbox.collections.item.Item
    
    .. autoproperty:: raw
    .. autoproperty:: string
    .. autoproperty:: integer
    .. autoproperty:: boolean
    .. autoproperty:: original

    The following special operators are included:

    .. automethod:: __pos__
    .. automethod:: __neg__

    The following operations are also included:

    .. function:: __contains__()

        .. code-block:: python

            b"hello" in Item("hello world") # >>> True

    .. function:: __eq__()

        .. code-block:: python

            Item(100) == Item(b'100') == Item('100') # >>> True

    .. function:: __add__()

        .. code-block:: python

            Item("hello") + Item("world") == Item("helloworld") # >>> True

    .. function:: __iadd__()

        .. code-block:: python

            i = Item("hello") 
            i += Item("world")
            i == Item("helloworld") # >>> True

    .. function:: __sub__()

        Uses ``bytes.replace`` to remove item.

        .. code-block:: python

            Item("helloworld") - Item("world") == Item("hello") # >>> True

    .. function:: __isub__()

        .. code-block:: python

            i = Item("helloworld") 
            i -= Item("world")
            i == Item("hello") # >>> True
    
    .. function:: __iter__()

        Returns string version of the item for iteration.

        .. code-block:: python

            for i in Item("hello world"):
                print(i)

            # >>> h
            # >>> e
            # >>> ...

    .. function:: __hash__()

        .. code-block:: python

            hash(Item(100)) == hash(b"100") # >>> True

    .. function:: __len__()

        .. code-block:: python

            len(Item("hello world")) == 11 # >>> True

    .. function:: __bool__()

        .. code-block:: python

            False == bool(Item(0)) == bool(Item("")) == bool(Item(b"")) == bool(Item(False)) == bool(Item(None)) # >>> True
            True == bool(Item(1)) == bool(Item("hello")) == bool(Item(b"hello")) == bool(Item(True)) # >>> True

    .. function:: __str__()

        Equivalent to the :py:attr:`string` property.

    .. function:: __repr__()

        .. code-block:: python

            repr(Item(100)) # >>> Item(bytes=b'100', str='100', int=100, bool=True, original_type=int)
            repr(Item(True)) # >>> Item(bytes=b'1', str='1', int=1, bool=True, original_type=bool)
            repr(Item("hello")) # >>> Item(bytes=b'hello', str='hello', int=None, bool=True, original_type=str)

    The following functions are included:

    .. automethod:: replace

----

*******
mapping
*******

.. code-block:: python

    from toolbox.collections import mapping

Since the mappings below are children class to :py:class:`dict`, they may all be initialized in three different ways:

.. code-block:: python

    from toolbox.collections.mapping import ObjectDict

    ObjectDict(hello="world", ola="mundo")
    ObjectDict({"hello":"world", "ola": "mundo"})
    ObjectDict({"hello":"world"}, ola="mundo")

Note that :py:class:`*Dict` types below can be combined together (as mixins) to create unique dictionary types.

.. code-block:: python

    from toolbox.collections.mapping import ObjectDict, UnderscoreAccessDict, FrozenDict

    class Dict(ObjectDict, UnderscoreAccessDict, FrozenDict):
        """ Frozen dictionary that allows object access with underscore access. """

    d = Dict({"hello world": "ola mundo", "100": "one hundred"})
    print(d)                # >>> <Dict {'hello world': 'ola mundo', '100': 'one hundred'}>
    print(d.hello_world)    # >>> ola mundo
    print(d._100)           # >>> one hundred

.. autoclass:: toolbox.collections.mapping.BaseDict()
.. autoclass:: toolbox.collections.mapping.BidirectionalDict(BaseDict)
.. autoclass:: toolbox.collections.mapping.ObjectDict(BaseDict)
.. autoclass:: toolbox.collections.mapping.OverloadedDict(BaseDict)
.. autoclass:: toolbox.collections.mapping.UnderscoreAccessDict(BaseDict)
.. autoclass:: toolbox.collections.mapping.FrozenDict(BaseDict)
.. autoclass:: toolbox.collections.mapping.ItemDict(BaseDict)

----

**********
namedtuple
**********

.. code-block:: python

    from toolbox.collections import namedtuple

.. autofunction:: toolbox.collections.namedtuple.nestednamedtuple

    .. autoclass:: toolbox.collections.namedtuple.fdict
