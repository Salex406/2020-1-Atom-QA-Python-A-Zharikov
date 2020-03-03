import pytest
from random import randint



@pytest.fixture()
def rand_int():
    return randint(0, 10)