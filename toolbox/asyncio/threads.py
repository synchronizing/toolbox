import asyncio
import contextvars
import functools
from typing import Any, Awaitable, Callable


async def to_thread(func: Callable, *args, **kwargs) -> Awaitable:
    """Asynchronously run function ``func`` in a separate thread.

    Any ``*args`` and ``**kwargs`` supplied for this function are directly passed
    to ``func``. Also, the current :class:`contextvars.Context` is propogated,
    allowing context variables from the main thread to be accessed in the
    separate thread.

    Return a coroutine that can be awaited to get the eventual result of *func*.

    Args:
        func: Synchronous function to create awaitable context with.
        args: Arguments to pass to ``func``.
        kwargs: Arguments to pass to ``func``.

    Note:
        This function is similar to Python 3.9 ``asyncio.to_thread()``, which can be found
        `here <https://github.com/python/cpython/blob/e9684fac5a158be9806304a676e619857520a4dc/Lib/asyncio/threads.py>`_,
        with slight modifications to make it backwards compatible.

    Example:

        .. code-block:: python

            from toolbox.asyncio.threads import to_thread
            import asyncio
            import time

            def func():
                time.sleep(2)
                return "Hello world"

            asyncio main():
                await to_thread(func)

            asyncio.run(main())
    """

    loop = asyncio.get_event_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)


def awaitable(func: Callable) -> Awaitable[Any]:
    """Decorator that converts a synchronous function into an asynchronous function.

    When decorator is used ``func`` becomes an awaitable. When awaited, the synchronous
    function runs in a seperate thread as to not block the event loop. This function
    leverages the :func:`toolbox.asyncio.threads.to_thread` function.

    Args:
        func: Synchronous function to create awaitable context with.

    Example:

        .. code-block:: python

            from toolbox.asyncio.threads import awaitable
            import asyncio
            import time

            @awaitable
            def func():
                time.sleep(2)
                return "Hello world"

            async def main():
                await func()

            asyncio.run(func())
    """

    async def wrapper(*args, **kwargs):
        return await to_thread(func, *args, **kwargs)

    return wrapper
