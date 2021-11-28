import asyncio
import ssl

import pytest
from toolbox import ClassTask, awaitable, tls_handshake, to_thread


class Test_patterns:
    class CT(ClassTask):
        def __init__(self, future: asyncio.Future, start: bool = False):
            super().__init__(
                self.run,
                log_start=lambda: print("Starting!"),
                log_stop=lambda: print("Stopping!"),
                start=start,
            )
            self.future = future

        async def run(self):
            await asyncio.sleep(1)
            self.future.set_result(True)

    @pytest.mark.asyncio
    async def test_start(self):
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        process = self.CT(future, start=True)
        assert process._task and not process._task.done()

        await asyncio.sleep(2)
        assert future.done() and future.result() == True

        process.stop()
        assert process._task and process._task.done()

    @pytest.mark.asyncio
    async def test_context_manager(self):
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        process = self.CT(future)
        async with process as prcss:
            assert prcss._task and not prcss._task.done()
            await asyncio.sleep(2)
            assert future.done() and future.result() == True

        assert process._task and process._task.done()


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
