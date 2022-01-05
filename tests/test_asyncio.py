import asyncio
from typing import Callable, Optional

import pytest
from toolbox import CoroutineClass, awaitable, tls_handshake, to_thread


class Test_patterns:
    class CC(CoroutineClass):
        def __init__(
            self,
            future: Optional[asyncio.Future] = None,
            start_callback: Callable = lambda: print("Starting!"),
            end_callback: Callable = lambda: print("Stopping!"),
            run: bool = False,
        ):
            super().__init__(
                start_callback=start_callback,
                end_callback=end_callback,
                run=run,
            )
            self.future = future

        async def entry(self):
            await asyncio.sleep(1)
            if isinstance(self.future, asyncio.Future):
                self.future.set_result(True)
            return self.future

    @pytest.mark.asyncio
    async def test_start(self):
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        process = self.CC(future, run=True)
        assert process._task and not process._task.done()

        await asyncio.sleep(2)
        assert future.done() and future.result() == True

        process.stop()
        assert process._task and process._task.done()

    @pytest.mark.asyncio
    async def test_await(self):
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        process = self.CC(future)
        await process
        assert future.done() and future.result() == True

    @pytest.mark.asyncio
    async def test_context_manager(self):
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        process = self.CC(future)
        async with process as prcss:
            assert prcss._task and not prcss._task.done()
            await asyncio.sleep(2)
            assert future.done() and future.result() == True

        assert process._task and process._task.done()

    @pytest.mark.asyncio
    async def test_callbacks(self):
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        # Start callback
        process = self.CC(future, run=future.set_result(None))
        process.run()
        assert future.done() and future.result() is None
        process.stop()

        # End callback.
        future = loop.create_future()
        process = self.CC(future, end_callback=future.set_result(None))
        process.run()
        process.stop()
        assert future.done() and future.result() is None

    def test_sync(self):
        process = self.CC(future=True)
        assert process.run() == process.result == True


class Test_streams:
    @pytest.mark.asyncio
    async def test_stream_client(self):
        reader, writer = await asyncio.open_connection("httpbin.org", 443, ssl=False)

        await tls_handshake(reader=reader, writer=writer)

        writer.write(
            b"GET /get HTTP/1.1\r\n"
            b"Host: httpbin.org\r\n"
            b"Keep-Alive: Close\r\n\r\n"
        )
        await writer.drain()

        data = await reader.read(1024)
        assert data.startswith(b"HTTP/1.1 200 OK")

        writer.close()
        await writer.wait_closed()


class Test_threads:
    @pytest.mark.asyncio
    async def test_threads_run(self):
        def func():
            return "hello world"

        assert await to_thread(lambda: func()) == "hello world"

    @pytest.mark.asyncio
    async def test_awaitable(self):
        @awaitable
        def func():
            return "hello world"

        assert await func() == "hello world"
