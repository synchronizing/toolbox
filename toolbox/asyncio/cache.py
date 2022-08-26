import asyncio
from functools import _make_key, wraps
from typing import Awaitable, Optional


def future_lru_cache(maxsize: Optional[int] = None) -> Awaitable:
    """
    Decorator to cache an async function's return value each time it is called.

    Args:
        maxsize: The maximum size of the cache.

    Returns:
        The decorated function.

    Notes:
        This method is a modification of a answer from StackOverflow
        `here <https://stackoverflow.com/a/37627076/1305461>`_.

    Example:

        .. code-block:: python

            from toolbox import future_lru_cache

            @future_lru_cache
            async def func():
                # Expensive computation.
                return 42

            async def main():
                await func()  # Runs it once.
                await func()  # Returns the cached value.
    """
    cache = {}

    async def run_and_cache(func, args, kwargs):
        """
        Run func with the specified arguments and store the result in cache.
        """
        result = await func(*args, **kwargs)
        cache[_make_key(args, kwargs, False)] = result
        if isinstance(maxsize, int) and len(cache) > maxsize:
            cache.popitem(False)
        return result

    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            key = _make_key(args, kwargs, False)
            if key in cache:
                # Some protection against duplicating calls already in
                # progress: when starting the call cache the future, and if
                # the same thing is requested again return that future.
                if isinstance(cache[key], asyncio.Future):
                    return cache[key]
                else:
                    f = asyncio.Future()
                    f.set_result(cache[key])
                    return f
            else:
                task = asyncio.Task(run_and_cache(func, args, kwargs))
                cache[key] = task
                return task

        return decorator

    if callable(maxsize):
        return wrapper(maxsize)
    else:
        return wrapper
