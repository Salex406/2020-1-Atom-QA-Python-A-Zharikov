import pytest
import sys


class TestSet:

    def test_instance(self):
        st = set()
        assert isinstance(st, set)

    def test_union(self):
        st1 = {1, 2, 3}
        st2 = set()
        assert st1 | st2 == st1

    @pytest.mark.parametrize('obj', [-sys.maxsize, -1, 0, 1,
                                     sys.maxsize, "a", b'x00', False])
    def test_adding(self, obj):
        st1 = set()
        st1.add(obj)
        assert obj in st1

    def test_difference(self):
        st1 = {1, sys.maxsize, 0, -40, 30}
        st2 = {0, sys.maxsize, 1, 60}
        assert st1.difference(st2) == {-40, 30}

    def test_remove(self, rand_int):
        st1 = set()
        with pytest.raises(KeyError):
            st1.remove(rand_int)
