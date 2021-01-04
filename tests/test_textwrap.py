from toolbox import unindent


class Test_text:
    def test_unindent(self):
        assert (
            unindent(
                """
            hello world
            this is a test
            """
            )
            == """hello world
this is a test"""
        )
