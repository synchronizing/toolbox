from toolbox.pkgutil.package import search_package
import pytest
import sys


class Test_package:
    def test_search_package(self):
        assert "toolbox" in search_package("toolbox", "is")
        assert "toolbox" in search_package("tool", "in")
        assert "toolbox" in search_package("tool", "startswith")

        search_package("toolbox", "is", imports=True)
        assert "toolbox" in sys.modules

        with pytest.raises(TypeError):
            search_package("toolbox", "hello")
