#######
asyncio
#######

*****
cache
*****

.. code-block:: python

    from toolbox.asyncio import future_lru_cache

.. autofunction:: toolbox.asyncio.future_lru_cache

----

*******
pattern
*******

.. code-block:: python

    from toolbox.asyncio import pattern

.. autoclass:: toolbox.asyncio.pattern.CoroutineClass

    .. autofunction:: toolbox.asyncio.pattern.CoroutineClass.start

    .. autofunction:: toolbox.asyncio.pattern.CoroutineClass.stop

----

*******
streams
*******

.. code-block:: python

    from toolbox.asyncio import streams

.. autofunction:: toolbox.asyncio.streams.tls_handshake

----

*******
threads
*******

.. code-block:: python

    from toolbox.asyncio import threads

.. autofunction:: toolbox.asyncio.threads.to_thread

.. autofunction:: toolbox.asyncio.threads.awaitable
