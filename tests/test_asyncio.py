from toolbox import to_thread, awaitable
import pytest


class Test_threads_to_thread:
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
