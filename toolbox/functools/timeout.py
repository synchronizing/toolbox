import asyncio
import datetime
import functools
import inspect
import signal
from typing import Awaitable, Callable, Union


def timeout(
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
    error: bool = False,
) -> Union[Callable, Awaitable]:
    """Wait for *time* before quitting *func* run and returning None.

    This decorator works with both asynchronous and synchronous functions. Note,
    however, that with synchronous function the *signal* module is used and
    therefore will not work with non-Unix based systems.

    Args:
        days: Days to wait before timeout.
        hours: Hours to wait before timeout.
        minutes: Minutes to wait before timeout.
        seconds: Seconds to wait before timeout.
        error: Indicates whether or not to throw ``TimeoutError`` error once function timeouts.

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
        """
        Wraps async or sync function with timeout functionality.
        """

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            """
            Leverages the asyncio.wait_for() function to wait for a given amount of time.
            """

            try:
                return await asyncio.wait_for(func(*args, **kwargs), total_seconds)
            except asyncio.TimeoutError as err:
                if error:
                    raise TimeoutError(
                        "Function {} timed out.".format(func.__name__)
                    ) from err

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            """
            Leverages the signal.alarm() function to wait for a given amount of time.
            """

            def _handle_timeout(signum, frame):
                raise TimeoutError

            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(total_seconds)
            try:
                return func(*args, **kwargs)
            except TimeoutError as err:
                if error:
                    raise TimeoutError(
                        "Function {} timed out.".format(func.__name__)
                    ) from err

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return wrapper
