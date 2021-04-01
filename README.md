# 🧰 Toolbox

<p align="center">

  <a href="https://github.com/shades-st/toolbox/actions?query=workflow%3ABuild">
    <img src="https://github.com/shades-st/toolbox/workflows/Build/badge.svg?branch=master&event=push">
  </a>

<a href="https://shades-st.github.io/toolbox/">
    <img src="https://github.com/shades-st/toolbox/workflows/Docs/badge.svg?branch=master&event=push">
  </a>

  <a href="https://coveralls.io/github/synchronizing/toolbox?branch=master">
    <img src="https://coveralls.io/repos/github/synchronizing/toolbox/badge.svg?branch=master">
  </a>

  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg">
  </a>
</p>

Toolbox is a set of tools that expands on the [Python Standard Library](https://docs.python.org/3/library/).

## Installing

```
pip install toolbox
```

## Documentation

Documentation can be found [**here**](http://shades-st.github.io/toolbox/). PDF version of docs can be found [here](https://shades-st.github.io/toolbox/toolbox.pdf).

# Tools

Toolbox follows the same pattern as of the Python Standard Library (PSL) which means that all tools are found inside package names that corresponds to that of the PSL (e.g. `asyncio`, `collections`, etc.) with only one exception (`config`).

## Code Examples

Check out documentation for function definitions and more details.

### `asyncio`

#### [`async to_thread`](https://shades-st.github.io/toolbox/module/asyncio.html#toolbox.asyncio.threads.to_thread)

Runs passed function in a new thread to ensure non-blocking IO during asynchronous programming.

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

#### [`awaitable`](https://shades-st.github.io/toolbox/module/asyncio.html#toolbox.asyncio.threads.awaitable)

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

### `builtins`

#### [`classproperty`](https://shades-st.github.io/toolbox/module/builtins.html#toolbox.builtins.property.classproperty)

Combines a `property` and a `classmethod` into one, creating a class property. Allows access to computed class attributes.

```python
from toolbox import classproperty

class Animal:
    @classproperty
    def dog(cls):
        return "whoof!"

print(Animal.dog) # >>> 'whoof!'
```


### `collections`

#### [`Item`](https://shades-st.github.io/toolbox/module/collections.html#toolbox.collections.item.Item)

An interface for type-agnostic operations between different types.

```python
from toolbox import Item

item = Item(100)
print(item == b"100" == "100" == 100) # >>> True
```

#### [`BidirectionalDict`](https://shades-st.github.io/toolbox/module/collections.html#toolbox.collections.mapping.BidirectionalDict)

Dictionary with two-way capabilities.

```python
from toolbox import BidirectionalDict

d = BidirectionalDict({"hello": "world"})
print(d) # >>> {'hello': 'world', 'world': 'hello'}
```

#### [`ObjectDict`](https://shades-st.github.io/toolbox/module/collections.html#toolbox.collections.mapping.ObjectDict)

Dictionary that can be accessed as though it was an object.

```python
from toolbox import ObjectDict

d = ObjectDict({"hello": "world"})
print(d.hello) # >>> 'world'
```

#### [`OverloadedDict`](https://shades-st.github.io/toolbox/module/collections.html#toolbox.collections.mapping.OverloadedDict)

Dictionary that can be added or subtracted to.

```python
from toolbox import OverloadedDict

d1 = OverloadedDict({"hello": "world"})
d2 = OverloadedDict({"ola": "mundo"})

d1 += d2
print(d1) # >>> {'hello': 'world', 'ola': 'mundo'}

d1 -= d2
print(d1) # >>> {'hello': 'world'}
```

#### [`UnderscoreAccessDict`](https://shades-st.github.io/toolbox/module/collections.html#toolbox.collections.mapping.UnderscoreAccessDict)

Dictionary that does not distinct between spaces and underscores.

```python
from toolbox import UnderscoreAccessDict

d = UnderscoreAccessDict({"hello world": "ola mundo"})
d['hello_world'] # >>> 'ola mundo'
```

#### [`FrozenDict`](https://shades-st.github.io/toolbox/module/collections.html#toolbox.collections.mapping.FrozenDict)

Dictionary that is frozen.

```python
from toolbox import FrozenDict

d = FrozenDict({"hello": "world"})
d['ola'] = 'mundo'
# >>> KeyError: 'Cannot set key and value because this is a frozen dictionary.'
```

#### [`ItemDict`](https://shades-st.github.io/toolbox/module/collections.html#toolbox.collections.mapping.ItemDict)

Dictionary that utilizes [`Item`](#Item) for key and values.

```python
from toolbox import ItemDict, Item

d = ItemDict({"100": "one hundred"})
print(d[100])                                          # >>> one hundred
print(d[100] == d['100'] == d[b'100'] == d[Item(100)]) # >>> True
```

All `*Dict` types above can be combined together (as mixins) to create unique dictionary types. Example:

```python
from toolbox import ObjectDict, UnderscoreAccessDict

class Dict(ObjectDict, UnderscoreAccessDict):
    """ New dictionary that allows object access with underscore access. """

d = Dict({"hello world": "ola mundo", "100": "one hundred"})
print(d.hello_world)    # >>> ola mundo
print(d._100)           # >>> one hundred
```

#### [`nestednamedtuple`](https://shades-st.github.io/toolbox/module/collections.html#toolbox.collections.namedtuple.nestednamedtuple)

Creates a nested `namedtuple` for easy object access.

```python
from toolbox import nestednamedtuple

nt = nestednamedtuple({"hello": {"ola": "mundo"}})
print(nt)           # >>> namedtupled(hello=namedtupled(ola='mundo'))
print(nt.hello.ola) # >>> mundo
```

#### [`fdict`](https://shades-st.github.io/toolbox/module/collections.html#toolbox.collections.namedtuple.fdict)

Forces `nestednamedtuple` to not convert `dict` to `namedtuple`. 

```python
from toolbox import nestednamedtuple

d = {"hello": "world"}
nt = nestednamedtuple({"forced": fdict(d), "notforced": d})

print(nt.notforced) # >>> namedtupled(hello='world')
print(nt.forced)    # >>> {'hello': 'world'}
```

### `config`

#### [`make_config`](https://shades-st.github.io/toolbox/module/config.html#toolbox.config.globalconfig.make_config)

Creates a global configuration that can be accessed by other portions of the code via `conf` or `config` function calls. Minimizes the need to create `Config` objects and pass them around different modules, classes, functions, etc.

```python
from toolbox import make_config

make_config(hello="world")
```

#### [`conf`](https://shades-st.github.io/toolbox/module/config.html#toolbox.config.globalconfig.conf)

Access global configuration as a `nestednamedtuple`.

```python
from toolbox import conf

print(conf().hello) # >>> 'world'
```

#### [`config`](https://shades-st.github.io/toolbox/module/config.html#toolbox.config.globalconfig.config)

Access global configuration as a dictionary.

```python
from toolbox import config

print(config()['hello']) # >>> 'world'
```

### `functools`

#### [`timeout`](https://shades-st.github.io/toolbox/module/functools.html#toolbox.functools.timeout.timeout)

Decorator that adds support for synchronous and asynchronous function timeout. Quits function after an amount of time passes.

```python
from toolbox import timeout

@timeout(seconds=5)
def func():
    time.wait(15)

func()
```

### `pkgutil`

#### [`search_package`](https://shades-st.github.io/toolbox/module/pkgutil.html#toolbox.pkgutil.package.search_package)

Searches for packages installed in the system.

```python
from toolbox import search_package

print(search_package("toolbox", method="is"))
# >>> {'toolbox': <module 'toolbox' from '.../toolbox/__init__.py'>}
```

### `experimental`

All tools marked as experimental are not meant to be used in production.

#### [`asyncdispatch`](https://shades-st.github.io/toolbox/module/experimental.html#toolbox.experimental.asyncdispatch.asyncdispatch)

Decorator for adding dispatch functionality between async and sync functions. Allows calling the same function name, one as a normal function and one as an awaitable, yet receive different results.

```python
from toolbox import asyncdispatch
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
```

### `string`

Comes out of the box with built-in ANSI formats that allows text style modification.

```python
from toolbox import bold, red

print(red("This text is red!"))
print(bold("This text is bolded!"))
```

Check documentation [here](https://shades-st.github.io/toolbox/module/string.html#color) for further information on all built-in formats.

#### [`Format`](https://shades-st.github.io/toolbox/module/string.html#toolbox.string.color.Format)

Persistent ANSI format container that allows custom ANSI code.

```python
from toolbox import Format

bold = Format(code=1)
print(bold("hello world"))
```

#### [`Style`](https://shades-st.github.io/toolbox/module/string.html#toolbox.string.color.Style)

Persistent ANSI format container that allows multiple ANSI codes.

```python
from toolbox import Style, red, bold

error = Style(red, bold)
print(error("This is red & bolded error."))
```

#### [`supports_color`](https://shades-st.github.io/toolbox/module/string.html#toolbox.string.color.supports_color)

Returns bool that indicates whether or not the user's terminal supports color.

```python
from toolbox import supports_color

print(supports_color())
```

#### [`strip_ansi`](https://shades-st.github.io/toolbox/module/string.html#toolbox.string.color.strip_ansi)

Removes ANSI codes from string.

```python
from toolbox import strip_ansi

print(strip_ansi("\x1b[1mhello world\x1b[0m")) # >>> hello world
```

### `textwrap`

#### [`unindent`](https://shades-st.github.io/toolbox/module/textwrap.html#toolbox.textwrap.text.unindent)

Unident triple quotes and removes any white spaces before or after text.

```python
from toolbox import unident

def test():
    return unindent(
        '''
        hello world
        this is a test
        of this functionality
        '''
    )

print(test()) 
# >>> hello world
# >>> this is a test
# >>> of this functionality
```
