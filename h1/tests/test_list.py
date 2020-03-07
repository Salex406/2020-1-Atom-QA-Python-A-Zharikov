import pytest


class TestList:

    def test_instance(self):
        lst = list()
        assert isinstance(lst, list)

    def test_insert(self, rand_int):
        lst = [i for i in range(0, rand_int)]
        lst.insert(1, False)
        assert lst[1] == False

    @pytest.mark.parametrize("l1", [[], ["123", "0"], [True, 5, (4, 6)]])
    def test_extend(self, l1):
        l2 = [[8, -9]]
        l1.extend(l2)
        assert [8, -9] in l1

    def test_multiply(self):
        l1 = [1, "fr"] * 3
        assert l1 == [1, "fr", 1, "fr", 1, "fr"]

    def test_length(self, rand_int):
        lst = [i for i in range(0, rand_int)]
        assert len(lst) == rand_int
