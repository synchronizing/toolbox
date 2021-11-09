import pytest
from toolbox import (
    BaseDict,
    BidirectionalDict,
    Item,
    ObjectDict,
    OverloadedDict,
    UnderscoreAccessDict,
    FrozenDict,
    ItemDict,
    fdict,
    nestednamedtuple,
)


class Test_item:
    def test_item_init(self):
        item = Item(100)
        assert item._item == b"100"
        assert item._type == int

    def test_item_properties(self):
        item1 = Item(100)
        assert item1._item == b"100"
        assert item1._type == int
        assert item1.raw == b"100"
        assert item1.string == "100"
        assert item1.integer == 100
        assert item1.boolean == True
        assert item1.original == 100

        item2 = Item("hello world")
        assert item2._item == b"hello world"
        assert item2._type == str
        assert item2.raw == b"hello world"
        assert item2.string == "hello world"
        assert item2.integer == None
        assert item2.boolean == True
        assert item2.original == "hello world"

        item3 = Item(None)
        assert item3._item == b""
        assert item3._type == type(None)
        assert item3.raw == b""
        assert item3.string == ""
        assert item3.integer == None
        assert item3.boolean == False
        assert item3.original == None

    def test_replace(self):
        item = Item("hello world")
        item = item.replace("hello", "ola")
        assert item == Item("ola world")

    def test_item_pos_and_neg(self):
        assert +Item("100") == "100"
        assert +Item(100) == "100"
        assert +Item(None) == ""
        assert +Item(True) == "1"

        assert -Item("100") == 100
        assert -Item(100) == 100
        assert -Item(None) == None
        assert -Item(False) == 0

    def test_item_contains(self):
        assert b"hello" in Item("hello world")
        assert 100 in Item("one hundred is 100")
        assert "ola" in Item(b"ola mundo")

    def test_item_eq(self):
        assert Item(100) == Item("100") == Item(b"100")
        assert Item("hello") == Item(b"hello")

    def test_item_add(self):
        assert Item("hello") + Item("world") == Item("helloworld")

    def test_item_iadd(self):
        item = Item("hello")
        item += Item("world")
        assert item == Item("helloworld")

    def test_item_sub(self):
        assert Item("helloworld") - Item("world") == Item("hello")

    def test_item_isub(self):
        item = Item("helloworld")
        item -= Item("world")
        assert item == Item("hello")

    def test_item_iter(self):
        for i1, i2 in zip(Item("hello"), "hello"):
            assert i1 == i2

    def test_item_hash(self):
        assert hash(b"hello") == hash(Item("hello")) == hash(Item(b"hello"))

    def test_item_len(self):
        assert len(Item(None)) == 0
        assert len(Item(123)) == 3
        assert len(Item("hello world")) == 11

    def test_item_bool(self):
        item = Item(100)
        assert bool(item) == item.boolean

    def test_item_str(self):
        item = Item(100)
        assert str(item) == item.string

    def test_item_repr(self):
        assert (
            repr(Item(100))
            == "Item(bytes=b'100', str='100', int=100, bool=True, original_type=int)"
        )
        assert (
            repr(Item(None))
            == "Item(bytes=b'', str='', int=None, bool=False, original_type=NoneType)"
        )
        assert (
            repr(Item(True))
            == "Item(bytes=b'1', str='1', int=1, bool=True, original_type=bool)"
        )
        assert (
            repr(Item("hello"))
            == "Item(bytes=b'hello', str='hello', int=None, bool=True, original_type=str)"
        )

    def test_item_byte_item_err(self):
        with pytest.raises(TypeError):
            Item.byte_item(1.5)


class Test_mapping:
    class Test_collection_base:
        def test_base_dict_repr(self):
            d = BaseDict({"hello": "world"})
            assert repr(d) == "<BaseDict {'hello': 'world'}>"

    class Test_collection_bidirectional:
        def test_bidirectional_dict_type(self):
            assert isinstance(BidirectionalDict(), dict)

        def test_bidirectional_dict_data(self):
            d = BidirectionalDict({"hello": "world"})
            assert d["hello"] == "world"
            assert d["world"] == "hello"

        def test_bidirectional_dict_setattr(self):
            d = BidirectionalDict({"hello": "world"})
            d["ola"] = "mundo"

            assert d["ola"] == "mundo"
            assert d["mundo"] == "ola"

        def test_bidirectional_dict_update(self):
            d = BidirectionalDict()
            d.update({"hello": "world"})
            assert d["hello"] == "world"
            assert d["world"] == "hello"

    class Test_collection_object:
        def test_object_dict_type(self):
            assert isinstance(ObjectDict(), dict)

        def test_object_dict_data(self):
            d = ObjectDict({"hello": "world"})
            assert d.hello == "world"

    class Test_collection_overloaded:
        def test_overloaded_dict_type(self):
            assert isinstance(OverloadedDict(), dict)

        def test_overloaded_data_add(self):
            d1 = OverloadedDict({"one": 1})
            d2 = OverloadedDict({"two": 2})

            assert (d1 + d2) == {"one": 1, "two": 2}

        def test_overloaded_data_iadd(self):
            d1 = OverloadedDict({"one": 1})
            d2 = OverloadedDict({"two": 2})
            d1 += d2
            assert d1 == {"one": 1, "two": 2}

        def test_overloaded_data_sub(self):
            d1 = OverloadedDict({"one": 1, "two": 2})
            d2 = OverloadedDict({"two": 2})

            assert (d1 - d2) == {"one": 1}

        def test_overloaded_data_isub(self):
            d1 = OverloadedDict({"one": 1, "two": 2})
            d2 = OverloadedDict({"two": 2})
            d1 -= d2
            assert d1 == {"one": 1}

    class Test_collection_underscore:
        def test_underscore_access_str(self):
            d = UnderscoreAccessDict(
                {
                    "hello world": "ola mundo",
                    "ola_mundo": "hello world",
                    "key": "value",
                    "100": "one hundred",
                }
            )
            assert d["hello_world"] == "ola mundo"
            assert d["ola_mundo"] == "hello world"
            assert d["key"] == "value"
            assert d["_100"] == "one hundred"

    class Test_collection_frozen:
        def test_frozen_init(self):
            d = FrozenDict({"hello": "world"})

            with pytest.raises(KeyError):
                d["ola"] = "mundo"

        def test_frozen_update(self):
            d = FrozenDict({"hello": "world"})

            with pytest.raises(KeyError):
                d.update({"ola": "mundo"})

    class Test_collection_item:
        def test_item_init(self):
            d = ItemDict({"100": "one hundred"})
            assert d["100"] == d[b"100"] == d[100] == d[Item(100)]

        def test_item_setitem(self):
            d = ItemDict()
            d[100] = "one hundred"
            assert d["100"] == d[b"100"] == d[100] == d[Item(100)]

        def test_item_delitem(self):
            d = ItemDict()
            d[100] = "one hundred"
            assert len(d) == 1
            del d[100]
            assert len(d) == 0

        def test_item_contains(self):
            d = ItemDict({"100": "one hundred"})
            assert "100" in d
            assert b"100" in d
            assert 100 in d
            assert Item(100) in d

        def test_item_update(self):
            d = ItemDict()
            d.update({"100": "one hundred"})
            assert "100" in d
            assert b"100" in d
            assert 100 in d
            assert Item(100) in d


class Test_namedtuple:
    def test_reg_nestednamedtuple(self):
        nt = nestednamedtuple({"d": {"hello": "world"}})
        assert isinstance(nt, tuple)
        assert isinstance(nt.d, tuple)
        assert nt.d.hello == "world"

    def test_reg_nestednamedtuple_list(self):
        nt = nestednamedtuple({"d": ["ola", {"hello": "world"}]})
        assert isinstance(nt, tuple)
        assert isinstance(nt.d, list)
        assert isinstance(nt.d[1], tuple)
        assert nt.d[1].hello == "world"

    def test_fdict_nestednamedtuple(self):
        nt = nestednamedtuple({"d": fdict({"hello": "world"})})
        assert isinstance(nt, tuple)
        assert isinstance(nt.d, dict)
        assert nt.d["hello"] == "world"
