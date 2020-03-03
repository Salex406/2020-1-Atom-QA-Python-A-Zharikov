import pytest


class TestDictionary:

    def test_instance(self):
        d = dict()
        assert isinstance(d, dict)

    def test_key_error(self, rand_int):
        d = {}
        with pytest.raises(KeyError):
            assert d[rand_int]

    @pytest.mark.parametrize('d1', [{"key1": 1, 2: "val1"}, {}])
    def test_copy(self, d1):
        d2 = d1.copy()
        assert d1 == d2

    @pytest.mark.parametrize('d1', [{"key1": 1, 2: "val1"}, {}])
    def test_clear(self, d1):
        print(d1)
        d1.clear()
        assert d1 == {}

    def test_update(self):
        d1 = {"key1": True, "key2": -5, "key3": [1, 0]}
        d2 = {3: 80}
        d1.update(d2)
        assert d1 == {"key1": True, 3: 80, "key2": -5, "key3": [1, 0]}
