import asyncio
import time

import pytest
from toolbox import timeout


class Test_sync_timeout:
    def test_timeout_sync_shorter_timeout_no_err(self):
        @timeout(seconds=1)
        def sync_time_sleep_10():
            time.sleep(10)
            return True

        start = time.time()
        ret = sync_time_sleep_10()
        end = time.time()

        assert end - start <= 1.5
        assert ret is None

    def test_timeout_sync_longer_timeout_no_err(self):
        @timeout(seconds=1)
        def sync_time_sleep_01():
            time.sleep(0.1)
            return True

        start = time.time()
        ret = sync_time_sleep_01()
        end = time.time()

        assert end - start <= 1.0
        assert ret is True

    def test_timeout_sync_shorter_timeout_with_err(self):
        @timeout(seconds=1, error=True)
        def sync_time_sleep_10():
            time.sleep(10)
            return True

        with pytest.raises(TimeoutError):
            sync_time_sleep_10()


class Test_async_timeout:
    @pytest.mark.asyncio
    async def test_timeout_async_shorter_timeout_no_err(self):
        @timeout(seconds=1)
        async def async_time_sleep_01():
            await asyncio.sleep(0.1)
            return True

        start = time.time()
        ret = await async_time_sleep_01()
        end = time.time()

        assert end - start <= 1.5
        assert ret is True

    @pytest.mark.asyncio
    async def test_timeout_async_longer_timeout_no_err(self):
        @timeout(seconds=0.1)
        async def async_time_sleep_10():
            await asyncio.sleep(10)
            return True

        start = time.time()
        ret = await async_time_sleep_10()
        end = time.time()

        assert end - start <= 1
        assert ret is None

    @pytest.mark.asyncio
    async def test_timeout_sync_shorter_timeout_with_err(self):
        @timeout(seconds=1, error=True)
        async def async_time_sleep_10():
            await asyncio.sleep(10)
            return True

        with pytest.raises(TimeoutError):
            await async_time_sleep_10()
