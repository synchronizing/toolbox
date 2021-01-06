###########
collections
###########

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

.. autoclass:: toolbox.collections.mapping.BidirectionalDict()
.. autoclass:: toolbox.collections.mapping.ObjectDict()
.. autoclass:: toolbox.collections.mapping.OverloadedDict()

----

**********
namedtuple
**********

.. code-block:: python

    from toolbox.collections import namedtuple

.. autofunction:: toolbox.collections.namedtuple.nestednamedtuple

    .. autofunction:: toolbox.collections.namedtuple.fdict
