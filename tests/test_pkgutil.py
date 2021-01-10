from toolbox.pkgutil.package import search_package
import pytest


class Test_package:
    def test_search_package(self):
        assert "toolbox" in search_package("toolbox", "is")
        assert "toolbox" in search_package("tool", "in")
        assert "toolbox" in search_package("tool", "startswith")

        with pytest.raises(TypeError):
            search_package("toolbox", "hello")
