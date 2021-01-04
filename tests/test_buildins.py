from toolbox import classproperty


class Test_property:
    def test_classproperty(self):
        class Test:
            @classproperty
            def var(cls):
                return "hello"

        assert Test.var == "hello"
