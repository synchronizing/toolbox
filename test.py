from toolbox import asyncdispatch
import asyncio


@asyncdispatch
def func():
    return "sync"


@func.register
async def _():
    return "async"


async def main():
    print(func())  # >>> sync
    print(await func())  # >>> async


asyncio.run(main())
