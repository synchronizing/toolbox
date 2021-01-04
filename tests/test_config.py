from collections import namedtuple

import pytest
from toolbox import conf, config, make_config


class Test_make_config:
    def test_conf_type(self):
        assert isinstance(conf(), tuple)

    def test_config_type(self):
        assert isinstance(config(), dict)

    def test_make_config_and_config(self):
        make_config(hello="world")
        assert config()["hello"] == "world"

    def test_make_config_and_conf(self):
        make_config(hello="world")
        assert conf().hello == "world"
