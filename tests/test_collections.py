from collections import namedtuple
from toolbox import (
    BidirectionalDict,
    ObjectDict,
    OverloadedDict,
    nestednamedtuple,
    fdict,
)
import pytest


class Test_mapping:
    class Test_collection_bidirectional:
        def test_bidirectional_dict_type(self):
            assert isinstance(BidirectionalDict(), dict)

        def test_bidirectional_dict_data(self):
            d = BidirectionalDict({"hello": "world"})
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
