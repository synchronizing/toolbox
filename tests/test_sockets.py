from toolbox.sockets.ip import is_ip


class Test_sockets:
    def test_is_ip(self):
        assert is_ip("127.0.0.1") is True
        assert is_ip("000.000.000.000") is True
        assert is_ip("localhost") is False
        assert is_ip("https://example.com") is False
