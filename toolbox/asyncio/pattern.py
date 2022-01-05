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

                from toolbox.asyncio.pattern import CoroutineClass
                import asyncio

                class AsyncClass(CoroutineClass):
                    def __init__(self, run: bool = False):
                        super().__init__(
                            self.entry,
                            start_callback=lambda: print("Starting!"),
                            end_callback=lambda: print("Stopping!"),
                            run=True,
                        )

                    async def entry(self):
                        print("Running the CoroutineClass.")
                        await asyncio.sleep(5)
                        print("Finished running the CoroutineClass.")
                        return "Returning from the CoroutineClass."

                async def test_async():
                    # Using CoroutineClass inside an async function does not block the main thread.
                    # The only way to force the main thread to wait is to await the CoroutineClass.
                    print("--- async ---\n")

                    # Use with __init__.
                    print("Running: __init__")
                    process = AsyncClass(run=True)
                    await asyncio.sleep(1)  # We do not 'await process'.
                    process.stop()
                    print("\n")

                    # Use with functions to start/stop.
                    print("Running: .run() & .stop()")
                    process = AsyncClass()
                    process.run()
                    await asyncio.sleep(1)  # We do not 'await process'.
                    process.stop()
                    print("\n")

                    # Use with context manager to start/stop. Notice this will block.
                    print("Running: async with")
                    async with AsyncClass() as process:
                        result = await process  # We do wait for process.
                    print(f"Returned: {result}\n")

                    # Awaits for the process to finish. Notice this will block.
                    print("await process")
                    process = AsyncClass()
                    result = await process  # We do wait for process.
                    print(f"Returned: {result}\n")

                def test_sync():
                    # Using CoroutineClass inside a sync function blocks the main thread.
                    # No need to wait for the CoroutineClass.
                    print("--- sync ---\n")

                    # Notice that this will block.
                    print("Running: __init__")
                    process = AsyncClass(run=True)
                    result = process.result
                    print(f"Returned: {result}\n")

                    # Notice that this will also block.
                    print("Running: .run()")
                    process = AsyncClass()
                    process.run()
                    result = process.result
                    print(f"Returned: {result}\n")

                asyncio.run(test_async())
                test_sync()

        """
        self._func = func if func else self.entry
        self._start_callback = start_callback
        self._end_callback = end_callback
        self._task = None
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:  # pragma: no cover
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        finally:
            self._loop = loop

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
        if not self._task or self._task.cancelled():
            if self._start_callback:
                self._start_callback()
            self._task = self._loop.create_task(self._func())
            self._task.add_done_callback(self.stop)
            if not self._loop.is_running():
                self._loop.run_until_complete(self._task)
                return self.result

    def stop(self, result: Optional[Any] = None) -> Any:
        """
        Stops the task without blocking.
        """
        if self._task and not self._task.cancelled():
            if self._end_callback:
                self._end_callback()
            self._task.cancel()

        self.result = None
        if self._task.done():
            try:
                self.result = self._task.result()
            except asyncio.CancelledError:  # pragma: no cover
                pass
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
        if self._task:
            return self._task.cancelled()

    def __await__(self):
        """
        Await the task.
        """
        if not self._task:
            self.run()
        return self._task.__await__()
