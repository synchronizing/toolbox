# 🧰 Toolbox

<p align="center">

  <a href="https://github.com/synchronizing/toolbox/actions?query=workflow%3ABuild">
    <img src="https://github.com/synchronizing/toolbox/workflows/Build/badge.svg?branch=master&event=push">
  </a>

<a href="https://synchronizing.github.io/toolbox/">
    <img src="https://github.com/synchronizing/toolbox/workflows/Docs/badge.svg?branch=master&event=push">
  </a>

  <a href="https://coveralls.io/github/synchronizing/toolbox?branch=master">
    <img src="https://coveralls.io/repos/github/synchronizing/toolbox/badge.svg?branch=master">
  </a>

  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg">
  </a>
</p>

Toolbox is a small (~0.2MB) set of tools that expands the [Python Standard Library](https://docs.python.org/3/library/).

## Installing

```
pip install toolbox
```

## Documentation

Documentation can be found [**here**](http://synchronizing.github.io/toolbox/).

## Using

### `asyncio`

#### [`async to_thread`](https://synchronizing.github.io/toolbox/module/asyncio.html#toolbox.asyncio.threads.to_thread)

Runs given function in a new thread during asynchronous IO.

```python
from toolbox import to_thread
import asyncio
import time

def func():
    time.sleep(2)
    return "Hello world"

async def main():
    await to_thread(func)

asyncio.run(main())
```

#### [`awaitable`](https://synchronizing.github.io/toolbox/module/asyncio.html#toolbox.asyncio.threads.awaitable)

Decorator that converts synchronous function into an asynchronous function. Leverages the `to_thread` function above.

```python
from toolbox import awaitable
import asyncio
import time

@awaitable
def func():
    time.sleep(2)
    return "Hello world"

async def main():
    await func()

asyncio.run(func())
```

#### [`tls_handshake`](https://synchronizing.github.io/toolbox/module/asyncio.html#toolbox.asyncio.streams.tls_handshake)

Performs TLS handshake on passed reader/writer stream.

```python
from toolbox.asyncio.streams import tls_handshake
import asyncio

async def client():
    reader, writer = await asyncio.open_connection("httpbin.org", 443, ssl=False)
    await tls_handshake(reader=reader, writer=writer)

    # Communication is now encrypted.

asyncio.run(client())
```

#### [`CoroutineClass`](https://synchronizing.github.io/toolbox/module/asyncio.html#toolbox.asyncio.pattern.CoroutineClass)

Pattern for creating a coroutine-like class that has multiple ways to start it.

```python
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
```

### `builtins`

#### [`classproperty`](https://synchronizing.github.io/toolbox/module/builtins.html#toolbox.builtins.property.classproperty)

Combines a `property` and a `classmethod` into one, creating a class property. Allows access to computed class attributes.

```python
from toolbox import classproperty

class Animal:
    @classproperty
    def dog(cls):
        return "whoof!"

print(Animal.dog) #  'whoof!'
```


### `collections`

#### [`Item`](https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.item.Item)

An interface for type-agnostic operations between different types.

```python
from toolbox import Item

item = Item(100)
print(item == b"100" == "100" == 100) #  True
```

#### [`BidirectionalDict`](https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.mapping.BidirectionalDict)

Dictionary with two-way capabilities.

```python
from toolbox import BidirectionalDict

d = BidirectionalDict({"hello": "world"})
print(d) #  {'hello': 'world', 'world': 'hello'}
```

#### [`ObjectDict`](https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.mapping.ObjectDict)

Dictionary that can be accessed as though it was an object.

```python
from toolbox import ObjectDict

d = ObjectDict({"hello": "world"})
print(d.hello) #  'world'
```

#### [`OverloadedDict`](https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.mapping.OverloadedDict)

Dictionary that can be added or subtracted to.

```python
from toolbox import OverloadedDict

d1 = OverloadedDict({"hello": "world"})
d2 = OverloadedDict({"ola": "mundo"})

d1 += d2
print(d1) #  {'hello': 'world', 'ola': 'mundo'}

d1 -= d2
print(d1) #  {'hello': 'world'}
```

#### [`UnderscoreAccessDict`](https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.mapping.UnderscoreAccessDict)

Dictionary that does not distinct between spaces and underscores.

```python
from toolbox import UnderscoreAccessDict

d = UnderscoreAccessDict({"hello world": "ola mundo"})
d['hello_world'] #  'ola mundo'
```

#### [`FrozenDict`](https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.mapping.FrozenDict)

Dictionary that is frozen.

```python
from toolbox import FrozenDict

d = FrozenDict({"hello": "world"})
d['ola'] = 'mundo'
#  KeyError: 'Cannot set key and value because this is a frozen dictionary.'
```

#### [`ItemDict`](https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.mapping.ItemDict)

Dictionary that utilizes [`Item`](#Item) for key and values.

```python
from toolbox import ItemDict, Item

d = ItemDict({"100": "one hundred"})
print(d[100])                                          #  one hundred
print(d[100] == d['100'] == d[b'100'] == d[Item(100)]) #  True
```

All `*Dict` types above can be combined together (as mixins) to create unique dictionary types. Example:

```python
from toolbox import ObjectDict, UnderscoreAccessDict

class Dict(ObjectDict, UnderscoreAccessDict):
    """ New dictionary that allows object access with underscore access. """

d = Dict({"hello world": "ola mundo", "100": "one hundred"})
print(d.hello_world)    #  ola mundo
print(d._100)           #  one hundred
```

#### [`nestednamedtuple`](https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.namedtuple.nestednamedtuple)

Creates a nested `namedtuple` for easy object access.

```python
from toolbox import nestednamedtuple

nt = nestednamedtuple({"hello": {"ola": "mundo"}})
print(nt)           #  namedtupled(hello=namedtupled(ola='mundo'))
print(nt.hello.ola) #  mundo
```

#### [`fdict`](https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.namedtuple.fdict)

Forces `nestednamedtuple` to not convert `dict` to `namedtuple`. 

```python
from toolbox import nestednamedtuple

d = {"hello": "world"}
nt = nestednamedtuple({"forced": fdict(d), "notforced": d})

print(nt.notforced) #  namedtupled(hello='world')
print(nt.forced)    #  {'hello': 'world'}
```

### `config`

#### [`make_config`](https://synchronizing.github.io/toolbox/module/config.html#toolbox.config.globalconfig.make_config)

Creates a global configuration that can be accessed by other portions of the code via `conf` or `config` function calls. Minimizes the need to create `Config` objects and pass them around different modules, classes, functions, etc.

```python
from toolbox import make_config

make_config(hello="world")
```

#### [`conf`](https://synchronizing.github.io/toolbox/module/config.html#toolbox.config.globalconfig.conf)

Access global configuration as a `nestednamedtuple`.

```python
from toolbox import conf

print(conf().hello) #  'world'
```

#### [`config`](https://synchronizing.github.io/toolbox/module/config.html#toolbox.config.globalconfig.config)

Access global configuration as a dictionary.

```python
from toolbox import config

print(config()['hello']) #  'world'
```

### `functools`

#### [`timeout`](https://synchronizing.github.io/toolbox/module/functools.html#toolbox.functools.timeout.timeout)

Decorator that adds support for synchronous and asynchronous function timeout. Quits function after an amount of time passes.

```python
from toolbox import timeout
import asyncio
import time

@timeout(seconds=1)
def func():
    time.sleep(15)

@timeout(seconds=1)
async def func():
    await asyncio.sleep(15)
```

### `pkgutil`

#### [`search_package`](https://synchronizing.github.io/toolbox/module/pkgutil.html#toolbox.pkgutil.package.search_package)

Searches for packages installed in the system.

```python
from toolbox import search_package

print(search_package("toolbox", method="is"))
#  {'toolbox': <module 'toolbox' from '.../toolbox/__init__.py'>}
```

### `sockets`

#### [`is_ip`](https://synchronizing.github.io/toolbox/module/sockets.html#toolbox.sockets.ip.is_ip)
 
Checks if a string is an IP address.

```python
from toolbox import is_ip

print(is_ip('127.0.0.1')) # True
print(is_ip('localhost'))  # False
```

### `string`

#### ANSI Formatting

```python
from toolbox import bold, red

print(red("This text is red!"))
print(bold("This text is bolded!"))
```

Check documentation [here](https://synchronizing.github.io/toolbox/module/string.html#color) for further information on all built-in formats.

##### [`Format`](https://synchronizing.github.io/toolbox/module/string.html#toolbox.string.color.Format)

Persistent ANSI formatter that takes a custom ANSI code.

```python
from toolbox import Format

bold = Format(code=1)
print(bold("hello world"))
```

##### [`Style`](https://synchronizing.github.io/toolbox/module/string.html#toolbox.string.color.Style)

Persistent ANSI formatter that allows multiple ANSI codes.

```python
from toolbox import Style, red, bold

error = Style(red, bold)
print(error("This is red & bolded error."))
```

##### [`supports_color`](https://synchronizing.github.io/toolbox/module/string.html#toolbox.string.color.supports_color)

Check's whether user's terminal supports color.

```python
from toolbox import supports_color

print(supports_color())
```

##### [`strip_ansi`](https://synchronizing.github.io/toolbox/module/string.html#toolbox.string.color.strip_ansi)

Removes ANSI codes from string.

```python
from toolbox import strip_ansi

print(strip_ansi("\x1b[1mhello world\x1b[0m")) #  hello world
```

### `textwrap`

#### [`unindent`](https://synchronizing.github.io/toolbox/module/textwrap.html#toolbox.textwrap.text.unindent)

Unindent triple quotes and removes any white spaces before or after text.

```python
from toolbox import unindent


def test():
    text = """
           hello world
           this is a test
           """
    print(text)

    text = unindent(
        """
        hello world
        this is a test
        """
    )
    print(text)


test()
#           hello world
#           this is a test
#
# hello world
# this is a test
```
