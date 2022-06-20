from toolbox.pdb.sprinkle import sprinkle


class Test_pdb:
    def test_sprinkle(self, capsys):
        print(sprinkle())

        line, file = capsys.readouterr().out.split(" ")
        assert line == "6"
        assert "toolbox/tests/test_pdb.py" in file
