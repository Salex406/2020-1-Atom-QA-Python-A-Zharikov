import sys
import pytest


class TestString:

    def test_instance(self):
        s = "test"
        assert isinstance(s, str)

    def test_refcount(self):
        s1 = "test1"
        cnt1 = sys.getrefcount(s1)
        s2 = s1
        cnt2 = sys.getrefcount(s1)
        assert cnt2 - cnt1 == 1

    @pytest.mark.parametrize('s', ["123", "0"])
    def test_isnumeric(self, s):
        assert s.isnumeric()

    def test_format(self, rand_int):
        s1 = "random number: %s" % rand_int
        s2 = "random number: {}".format(rand_int)
        s3 = f"random number: {rand_int}"
        assert s1 == s2 == s3

    def test_count(self):
        s = "tft-0 t"
        assert s.count("t") == 3
