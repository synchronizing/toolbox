from typing import Union, Awaitable, Callable
import functools
import datetime
import inspect
import asyncio
import signal


def timeout(
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
    err: bool = False,
):
    """Wait for *time* before quitting *func* run and returning None.

    This decorator works with both asynchronous and synchronous functions. Note,
    however, that with synchronous function the *signal* module is used and
    therefore will not work with non-Unix based systems.

    Example:

        .. code-block:: python

            from toolbox.functools.timeout import timeout

            @timeout(seconds=5)
            def func():
                time.wait(15)

            func()
    """

    td = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    total_seconds = int(td.total_seconds())

    def wrapper(func: Union[Callable, Awaitable]):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), total_seconds)
            except asyncio.TimeoutError as error:
                if err:
                    raise TimeoutError(
                        "Function {} timed out.".format(func.__name__)
                    ) from error
                else:
                    return None

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            def _handle_timeout(signum, frame):
                raise TimeoutError

            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(total_seconds)
            try:
                return func(*args, **kwargs)
            except TimeoutError as error:
                if err:
                    raise TimeoutError(
                        "Function {} timed out.".format(func.__name__)
                    ) from error
                else:
                    return None

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return wrapper
