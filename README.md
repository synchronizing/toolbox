# 🧰 Toolbox

Toolbox is a set of tools that expands on the [Python Standard Library](https://docs.python.org/3/library/).

## Installing

```
pip install toolbox
```

## Documentation

Documentation can be found [here](http://synchronizing.github.io/toolbox/).


# Tools

Toolbox follows the same pattern as of the Python Standard Library (PSL) which means that all tools are found inside package names that corresponds to that of the PSL (e.g. `asyncio`, `collections`, etc.) with only one exception (`config`).

The following packages and tools are included:

* [`asyncio`](#asyncio)
    * `to_thread`
    * `awaitable`
* [`builtins`](#builtins)
    * `classproperty`
* [`collections`](#collections)
    * `BidirectionalDict`
    * `ObjectDict`
    * `OverloadedDict`
    * `nestednamedtuple`
* [`config`](#config)
    * `make_config`
    * `conf`
    * `config`
* [`experimental`](#experimental)
    * `asyncdispatch`
* [`functools`](#functools)
    * `timeout`
* [`textwrap`](#textwrap)
    * `unindent`

## Code Examples

Check out documentation for function definitions and more details.

### `asyncio`

#### [`async to_thread`](https://synchronizing.github.io/toolbox/module/asyncio.html#toolbox.asyncio.threads.to_thread)

Asynchronously run function func in a separate thread.

```python
from toolbox import to_thread
import asyncio
import time

def func():
    time.sleep(2)
    return "Hello world"

asyncio main():
    await to_thread(func)

asyncio.run(main())
```

#### [`awaitable`](https://synchronizing.github.io/toolbox/module/asyncio.html#toolbox.asyncio.threads.awaitable)

Decorator that converts a synchronous function into an asynchronous function by leveraging `to_thread` and sending function to a new thread on execution.

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

#### [`classproperty`](https://synchronizing.github.io/toolbox/module/builtins.html#toolbox.builtins.property.classproperty)

Combines a property and a classmethod into one, creating a class property. Allows access to computed class attributes.

```python
from toolbox import classproperty

class Animal:
    @classproperty
    def dog(cls):
        return "whoof!"

print(Animal.dog) # >>> 'whoof!'
```

### `collections`

#### [`BidirectionalDict`](https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.mapping.BidirectionalDict)

Dictionary with two-way capabilities.

```python
from toolbox import BidirectionalDict

d = BidirectionalDict({"hello": "world"})
print(d) # >>> {'hello': 'world', 'world': 'hello'}
```

#### [`ObjectDict`](https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.mapping.ObjectDict)

Dictionary that can be accessed as though it was an object.

```python
from toolbox import ObjectDict

d = ObjectDict({"hello": "world"})
print(d.hello) # >>> 'world'
```

#### [`OverloadedDict`](https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.mapping.OverloadedDict)

Dictionary that can be added or subtracted.

```python
from toolbox import OverloadedDict

d1 = OverloadedDict({"hello": "world"})
d2 = OverloadedDict({"ola": "mundo"})

d1 += d2
print(d1) # >>> {'hello': 'world', 'ola': 'mundo'}

d1 -= d2
print(d1) # >>> {'hello': 'world'}
```

#### [`nestednamedtuple`](https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.namedtuple.nestednamedtuple)

```python
nt = nestednamedtuple({"hello": {"ola": "mundo"}})
print(nt) # >>> namedtupled(hello=namedtupled(ola='mundo'))
```

#### [`fdict`](https://synchronizing.github.io/toolbox/module/collections.html#toolbox.collections.namedtuple.fdict)

```python
d = {"hello": "world"}
nt = nestednamedtuple({"forced": fdict(d), "notforced": d})

print(nt.notforced)    # >>> namedtupled(hello='world')
print(nt.forced)       # >>> {'hello': 'world'}
```

### `config`

#### [`make_config`](https://synchronizing.github.io/toolbox/module/config.html#toolbox.config.globalconfig.make_config)

Creates global configuration.

```python
from toolbox import make_config

make_config(hello="world")
```

#### [`conf`](https://synchronizing.github.io/toolbox/module/config.html#toolbox.config.globalconfig.conf)

Access global configuration as a nestednamedtuple.

```python
from toolbox import conf

print(conf().hello) # >>> 'world'
```

#### [`config`](https://synchronizing.github.io/toolbox/module/config.html#toolbox.config.globalconfig.config)

Access global configuration as a dictionary.

```python
from toolbox import config

print(config()['hello']) # >>> 'world'
```

### `functools`

#### [`timeout`](https://synchronizing.github.io/toolbox/module/functools.html#toolbox.functools.timeout.timeout)

Wait for time before quitting func run and returning None.

```python
from toolbox import timeout

@timeout(seconds=5)
def func():
    time.wait(15)

func()
```

### `experimental`

#### [`asyncdispatch`](https://synchronizing.github.io/toolbox/module/experimental.html#toolbox.experimental.asyncdispatch.asyncdispatch)

Decorator for adding dispatch functionality between async and sync functions.

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

### `textwrap`

#### [`unindent`](https://synchronizing.github.io/toolbox/module/textwrap.html#toolbox.textwrap.text.unindent)

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
