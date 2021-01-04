import asyncio
import contextvars
import functools


async def to_thread(func, *args, **kwargs):
    """Asynchronously run function *func* in a separate thread.

    Any *args and **kwargs supplied for this function are directly passed
    to *func*. Also, the current :class:`contextvars.Context` is propogated,
    allowing context variables from the main thread to be accessed in the
    separate thread.

    Return a coroutine that can be awaited to get the eventual result of *func*.

    Note:
        This function is similar to Python 3.9 'asyncio.to_thread()', which can be found here,
        with slight modifications to make it backwards compatible.

        https://github.com/python/cpython/blob/e9684fac5a158be9806304a676e619857520a4dc/Lib/asyncio/threads.py

    Example:

        .. code-block:: python

            from toolbox import to_thread
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


def awaitable(func):
    """Decorator that converts a synchronous function into an asynchronous function.

    When decorator is used *func* becomes an awaitable. When awaited, the synchronous
    function runs in a seperate thread as to not block the event loop. This function
    leverages the :func:`to_thread` function.

    Example:

        .. code-block:: python

            from toolbox import awaitable
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
