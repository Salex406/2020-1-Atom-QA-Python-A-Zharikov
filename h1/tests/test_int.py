import pytest
import sys


class TestInteger:

    def test_instance(self, rand_int):
        assert isinstance(rand_int, int)

    def test_coercion(self):
        s = "something"
        with pytest.raises(ValueError):
            assert int(s)

    @pytest.mark.parametrize('var', [-sys.maxsize, -1, 0, 1, sys.maxsize])
    def test_zero_div(self, var):
        with pytest.raises(ZeroDivisionError):
            assert var / 0

    def test_from_to_btes(self, rand_int):
        b = rand_int.to_bytes(rand_int.bit_length(), byteorder="big")
        assert rand_int == int.from_bytes(b, byteorder="big")

    def test_swap(self):
        a = 5
        b = 9
        a, b = b, a
        assert (a == 9) and (b == 5)
