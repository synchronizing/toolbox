import asyncio
from typing import Awaitable, Callable, Optional


class ClassTask:
    def __init__(
        self,
        func: Awaitable,
        log_start: Optional[Callable] = None,
        log_stop: Optional[Callable] = None,
        start: bool = False,
    ):
        """
        Adds start, stop, and async context manager functionality to a class.

        This is a useful pattern that can be used for any asyncio-based class with an
        awaitable entry-point that needs to be started/stopped via non-blocking code,
        and/or needs to be accessed via an async context manager.

        This is useful for large asynchronous operations that happens within a single
        class. See example below for how to use it.

        Args:
            func: The awaitable entry-point of the class.
            log_start: A function to call when the class is started.
            log_stop: A function to call when the class is stopped.
            start: Whether to start the class immediately on initialization.

        Example:

            .. code-block:: python

                from toolbox.asyncio.pattern import ClassTask
                import asyncio

                class AsyncClass(ClassTask):
                    def __init__(self, start: bool = False):
                        super().__init__(
                            self.run,
                            log_start=lambda: print("Starting!"),
                            log_stop=lambda: print("Stopping!"),
                            start=start,
                        )

                    async def run(self):
                        # Some async functionality here.

                async def main():

                    # Use with __init__ start.
                    process = AsyncClass(start=True)
                    await asyncio.sleep(1)
                    process.stop()

                    # Use with functions to start/stop.
                    process = AsyncClass()
                    process.start()
                    await asyncio.sleep(1)
                    process.stop()

                    # Use with context manager to start/stop.
                    async with AsyncClass() as process:
                        ...

                asyncio.run(main())
        """

        self._func = func
        self._log_start = log_start
        self._log_stop = log_stop
        self._task = None
        self._loop = asyncio.get_event_loop()
        if start:
            self.start()

    def start(self):
        """
        Starts the task without blocking.
        """
        if not self._task or self._task.cancelled():
            if self._log_start:
                self._log_start()
            self._task = self._loop.create_task(self._func())

    def stop(self):
        """
        Stops the task without blocking.
        """
        if self._task and not self._task.cancelled():
            if self._log_stop:
                self._log_stop()
            self._task.cancel()

    async def __aenter__(self) -> type:
        self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.stop()
        if self._task:
            return self._task.cancelled()
