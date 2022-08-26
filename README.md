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

## Tools

### `asyncio`

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/asyncio.html#toolbox.asyncio.cache.future_lru_cache"><code>future_lru_cache</code></a> — <code>lru_cache</code> for async functions.</summary><br>
  
```python
from toolbox import future_lru_cache
import asyncio

@future_lru_cache
async def func():
    await asyncio.sleep(10)
    return 42

async def main():
    await func() # Runs once.
    await func() # Returns cached value.

asyncio.run(main())
````
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/asyncio.html#toolbox.asyncio.threads.to_thread"><code>to_thread</code></a> — Run a synchronous function in a separate thread.</summary><br>

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
````

</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/asyncio.html#toolbox.asyncio.threads.awaitable"><code>awaitable</code></a> — Convert synchronous function to an async function via thread.</summary><br>
  
Leverages the `to_thread` function above.

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
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/asyncio.html#toolbox.asyncio.streams.tls_handshake"><code>tls_handshake</code></a> — Perform TLS handshake with a stream reader & writer.</summary><br>

```python
from toolbox import tls_handshake
import asyncio

async def client():
    reader, writer = await asyncio.open_connection("httpbin.org", 443, ssl=False)
    await tls_handshake(reader=reader, writer=writer)

    # Communication is now encrypted.

asyncio.run(client())
```
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/asyncio.html#toolbox.asyncio.pattern.CoroutineClass"><code>CoroutineClass</code></a> — Class pattern for implementing object-based coroutines. </summary><br>
  
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
</details>

### `builtins`

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/builtins.html#toolbox.builtins.property.classproperty"><code>classproperty</code></a> — Decorator for defining a method as a property and classmethod.</summary><br>

Allows access to computed class attributes.

```python
from toolbox import classproperty

class Animal:
    @classproperty
    def dog(cls):
        return "whoof!"

print(Animal.dog) #  'whoof!'
```
</details>

### `collections`

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.item.Item"><code>Item</code></a> — An interface for type-agnostic operations between different types.</summary><br>

```python
from toolbox import Item

item = Item(100)
print(item == b"100" == "100" == 100) #  True
```
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.namedtuple.nestednamedtuple"><code>nestednamedtuple</code></a> — Creates a nested <code>namedtuple</code>.</summary><br>

```python
from toolbox import nestednamedtuple

nt = nestednamedtuple({"hello": {"ola": "mundo"}})
print(nt)           #  namedtupled(hello=namedtupled(ola='mundo'))
print(nt.hello.ola) #  mundo
```
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.namedtuple.fdict"><code>fdict</code></a> — Forces <code>nestednamedtuple</code> to not convert <code>dict</code> to <code>namedtuple</code>. </summary><br>

```python
from toolbox import nestednamedtuple, fdict

d = {"hello": "world"}
nt = nestednamedtuple({"forced": fdict(d), "notforced": d})

print(nt.notforced) #  namedtupled(hello='world')
print(nt.forced)    #  {'hello': 'world'}
```
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.item.Item"><code>BidirectionalDict</code></a> — Dictionary with two-way capabilities.</summary><br>

```python
from toolbox import BidirectionalDict

d = BidirectionalDict({"hello": "world"})
print(d) #  {'hello': 'world', 'world': 'hello'}
```
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.mapping.ObjectDict"><code>ObjectDict</code></a> — Dictionary that can be accessed as though it was an object.</summary><br>

```python
from toolbox import ObjectDict

d = ObjectDict({"hello": "world"})
print(d.hello) #  'world'
```
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.mapping.OverloadedDict"><code>OverloadedDict</code></a> — Dictionary that can be added or subtracted to.</summary><br>

```python
from toolbox import OverloadedDict

d1 = OverloadedDict({"hello": "world"})
d2 = OverloadedDict({"ola": "mundo"})

d1 += d2
print(d1) #  {'hello': 'world', 'ola': 'mundo'}

d1 -= d2
print(d1) #  {'hello': 'world'}
```
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.mapping.UnderscoreAccessDict"><code>UnderscoreAccessDict</code></a> — Dictionary with underscore access.</summary><br>

```python
from toolbox import OverloadedDict

d1 = OverloadedDict({"hello": "world"})
d2 = OverloadedDict({"ola": "mundo"})

d1 += d2
print(d1) #  {'hello': 'world', 'ola': 'mundo'}

d1 -= d2
print(d1) #  {'hello': 'world'}
```
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.mapping.FrozenDict"><code>FrozenDict</code></a> — Dictionary that is frozen.</summary><br>

```python
from toolbox import OverloadedDict

d1 = OverloadedDict({"hello": "world"})
d2 = OverloadedDict({"ola": "mundo"})

d1 += d2
print(d1) #  {'hello': 'world', 'ola': 'mundo'}

d1 -= d2
print(d1) #  {'hello': 'world'}
```
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.mapping.ItemDict"><code>ItemDict</code></a> — Dictionary that utilizes <a href="#Item"><code>Item</code></a> for key and values.</summary><br>

```python
from toolbox import ItemDict, Item

d = ItemDict({"100": "one hundred"})
print(d[100])                                          #  one hundred
print(d[100] == d['100'] == d[b'100'] == d[Item(100)]) #  True
```
</details>

All `*Dict` types above can be combined together (as mixins) to create unique dictionary types.

### `config`

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/config.html#toolbox.config.globalconfig.make_config"><code>make_config</code></a> — Stores configuration dictionary in-memory.</summary><br>

Creates a global configuration that can be accessed by other portions of the code via `conf` or `config` function calls. Minimizes the need to create `Config` objects and pass them around different modules, classes, functions, etc.

```python
from toolbox import make_config

make_config(hello="world")
```
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/config.html#toolbox.config.globalconfig.config"><code>config</code></a> — Access in-memory configuration as dictionary.</summary><br>

```python
from toolbox import config

print(config()['hello']) #  'world'
```
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/config.html#toolbox.config.globalconfig.conf"><code>conf</code></a> — Access in-memory configuration as <code>nestednametuple</code>.</summary><br>

```python
from toolbox import conf

print(conf().hello) #  'world'
```
</details>

### `functools`

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/functools.html#toolbox.functools.timeout.timeout"><code>timeout</code></a> — Decorator to add timeout for synchronous and asychronous functions.</summary><br>

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
</details>

### `pdb`

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/pdb.html#toolbox.pdb.sprinke.sprinkle"><code>sprinkle</code></a> —  Prints the line and file that this function was just called from.</summary><br>

```python
from toolbox.pdb.sprinkle import sprinkle

sprinkle() # >>> 3 this_file.py
sprinkle("hello", "world") # >>> 4 this_file.py hello world
```
</details>

### `pkgutil`

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/pkgutil.html#toolbox.pkgutil.package.search_package"><code>search_package</code></a> — Searches for packages installed in the system.</summary><br>

```python
from toolbox import search_package

print(search_package("toolbox", method="is"))
#  {'toolbox': <module 'toolbox' from '.../toolbox/__init__.py'>}
```
</details>

### `sockets`

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/sockets.html#toolbox.sockets.ip.is_ip"><code>is_ip</code></a> — Checks if a string is an IP address.</summary><br>

```python
from toolbox import is_ip

print(is_ip('127.0.0.1')) # True
print(is_ip('localhost')) # False
```
</details>

### `string`

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/string.html#color">ANSI Formatting</a> — Color formatting.</summary><br>

Check documentation [here](https://synchronizing.github.io/toolbox/module/string.html#color) for further information on all built-in formats.

```python
from toolbox import bold, red

print(red("This text is red!"))
print(bold("This text is bolded!"))
```
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/string.html#toolbox.string.color.Format"><code>Format</code></a> — Persistent ANSI formatter that takes a custom ANSI code.</summary><br>

```python
from toolbox import Format

bold = Format(code=1)
print(bold("hello world"))
```
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/string.html#toolbox.string.color.Style"><code>Style</code></a> — Persistent ANSI formatter that allows multiple ANSI codes.</summary><br>

```python
from toolbox import Style, red, bold

error = Style(red, bold)
print(error("This is red & bolded error."))
```
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/string.html#toolbox.string.color.supports_color"><code>supports_color</code></a> — Check's if the user's terminal supports color.</summary><br>

```python
from toolbox import supports_color

print(supports_color()) # True
```
</details>

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/string.html#toolbox.string.color.strip_ansi"><code>strip_ansi</code></a> — Removes ANSI codes from string.</summary><br>

```python
from toolbox import strip_ansi

print(strip_ansi("\x1b[1mhello world\x1b[0m")) #  hello world
```
</details>

### `textwrap`

<details>
  <summary><a href="https://synchronizing.github.io/toolbox/module/textwrap.html#toolbox.textwrap.text.unindent"><code>unindent</code></a> — Removes indent and white-space from docstrings.</summary><br>

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
</details>
