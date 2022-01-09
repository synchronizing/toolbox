import asyncio
from abc import ABC
from typing import Any, Awaitable, Callable, Optional


class CoroutineClass(ABC):
    def __init__(
        self,
        func: Optional[Awaitable] = None,
        start_callback: Optional[Callable] = None,
        end_callback: Optional[Callable] = None,
        run: bool = False,
    ):
        """
        Adds start, stop, and async context manager functionality to a class.

        This is a useful pattern that can be used for any asyncio-based class with an
        awaitable entry-point that needs to be started/stopped via both non-blocking
        code, and/or async code. Built-in with an async context manager.

        This is useful for large asynchronous operations that happens within a single
        class. See example below for how to use it.

        Args:
            func: The awaitable entry-point of the class. Defaults to 'self.entry'.
            start_callback: A function to call when the class is started.
            end_callback: A function to call when the class is stopped.
            run: Whether to start the class immediately on initialization.

        Example:

            .. code-block:: python

                from toolbox import CoroutineClass
                import asyncio

                class Coroutine(CoroutineClass):
                    def __init__(self, run: bool = False):
                        super().__init__(run=run)

                    # Default entry function.
                    async def entry(self):
                        await asyncio.sleep(1)
                        return "Hello world"

                # Start coroutine outside Python async context.
                def iomain():

                    # via __init__
                    coro = Coroutine(run=True)
                    print(coro.result)  # Hello world

                    # via .run()
                    coro = Coroutine()
                    result = coro.run()
                    print(result)  # Hello world

                # Start coroutine inside Python async context.
                async def aiomain():

                    # via __init__
                    coro = Coroutine(run=True)
                    await asyncio.sleep(1)
                    coro.stop()
                    print(coro.result)  # None - because process was stopped before completion.

                    # via .run()
                    coro = Coroutine()
                    coro.run()
                    await asyncio.sleep(1)
                    result = coro.stop()  # None - because coroutine was stopped before completion.
                    print(result)  # Hello world

                    # via await
                    coro = Coroutine()
                    result = await coro  # You can also start, and await later.
                    print(result)  # Hello World

                    # via context manager
                    async with Coroutine() as coro:
                        result = await coro
                    print(result)  # Hello World

        """
        self._func = func if func else self.entry
        self._start_callback = start_callback
        self._end_callback = end_callback
        self._task = None

        # Setup the asyncio loop.
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:  # pragma: no cover
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        finally:
            self._loop = loop

        self.result = None

        if run:
            self.run()

    async def entry(self):
        """
        Default async entry-point.
        """
        raise NotImplementedError  # pragma: no cover

    def run(self):
        """
        Starts the task without blocking.

        Note:
            The task will block if we call this method outside an async context.
        """

        # If task is not running or has been cancelled, start it.
        if not self._task or self._task.cancelled():

            # Call the start callback.
            if self._start_callback:
                self._start_callback()

            # Creates the task inside the loop.
            self._task = self._loop.create_task(self._func())

            # Add self.stop as callback for when the task is done.
            self._task.add_done_callback(self.stop)

            # Runs the loop if we are not in an async context.
            if not self._loop.is_running():
                # Runs task until completion. Calls self.stop.
                self._loop.run_until_complete(self._task)
                return self.result

    def stop(self, result: Optional[Any] = None) -> Any:
        """
        Stops the task without blocking.

        Notes:
            This function is attached as a callback to the task.
        """

        # If task is running and hasn't been cancelled, cancel it.
        if self._task and not self._task.cancelled():

            # Cancel task.
            self._task.cancel()

            # Call the end callback.
            if self._end_callback:
                self._end_callback()

        # Tries the get the result of the task.
        if self._task.done():
            try:
                self.result = self._task.result()
            except asyncio.CancelledError:  # pragma: no cover
                pass

            # Return the result.
            return self.result

    async def __aenter__(self) -> type:
        """
        Enter the async context manager.
        """
        self.run()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Exit the async context manager.
        """
        return self._task.cancelled()

    def __await__(self):
        """
        Await the task.
        """
        if not self._task:
            self.run()
        return self._task.__await__()
