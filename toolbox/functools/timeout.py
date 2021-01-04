import functools
import datetime
import inspect
import asyncio
import signal


def timeout(days=0, hours=0, minutes=0, seconds=0, err=False):
    """Wait for *time* before quitting *func* run and returning None.

    This decorator works with both asynchronous and synchronous functions. Note,
    however, that with synchronous function the *signal* module is used and
    therefore will not work with non-Unix based systems.

    Example:

        .. code-block:: python

            from toolbox import timeout

            @timeout(seconds=5)
            def func():
                time.wait(15)

            func()
    """

    td = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    total_seconds = int(td.total_seconds())

    def wrapper(func):
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
