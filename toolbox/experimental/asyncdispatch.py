import ast
import functools
import inspect
import textwrap
from typing import Awaitable, Callable, Union


def asyncdispatch(func: Callable) -> Callable:
    """Decorator for adding dispatch functionality between async and sync functions.

    Similar to :py:func:`functools.singledispatch`, but for sync and async function. This
    decorator allows for a single function name to be used for two different implementations,
    one synchronous and another asynchronous. Note that in the implementation of
    :func:`asyncdispatch` the ``inspect`` module is utilized, and therefore might not work with
    different implementations of Python.

    Args:
        func: Synchronous function to create a dispatch with.

    Warning:
        Not recommended to be used in production in its current implementation.

    Example:

        .. code-block:: python

            from toolbox.experimental.asyncdispatch import asyncdispatch
            import asyncio

            @asyncdispatch
            def func():
                return "sync"

            @func.register
            async def _():
                return "async"

            async def main():
                print(func())          # >>> sync
                print(await func())    # >>> async

            asyncio.run(main())
    """

    funcs = {"sync": lambda: True, "async": lambda: True}

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Union[Callable, Awaitable]:

        # Gets the location where the function was called from.
        info = inspect.stack()[1]
        unindent = textwrap.dedent(info.code_context[0])
        tree = ast.parse(unindent)

        # Walks through ast.
        parent = None
        for node in ast.walk(tree):

            # Saves parent to the child node.
            if parent:
                node.parent = parent

            # Gets ast node where function is being called from.
            if "id" in node.__dict__ and node.id == func.__name__:

                # Checks if parent of parent of node is awaited.
                call = node.parent.parent
                if "parent" in call.__dict__ and isinstance(call.parent, ast.Await):
                    sync = False
                else:
                    sync = True

                # Breaks out of loop if function is found in ast.
                break

            # Saves new parent as old node.
            parent = node

        # Returns correct function depending if 'await' was present or not.
        if sync:
            return funcs["sync"](*args, **kwargs)
        else:
            return funcs["async"](*args, **kwargs)

    def register(func: Awaitable) -> None:
        # Register the functions accordingly.
        if inspect.iscoroutinefunction(func):
            funcs["async"] = func
        else:
            funcs["sync"] = func

    # Replace functions with wrapper.
    wrapper.register = register
    wrapper.register(func)
    return wrapper
