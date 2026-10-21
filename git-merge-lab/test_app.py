# test_app.py
import pytest

from app import add_numbers
from app import divide_numbers

def test_add_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0


def test_divide_numbers():
    assert divide_numbers(10, 2) == 5
    assert divide_numbers(-9, 3) == -3
    assert divide_numbers(7, 2) == 3.5
    assert divide_numbers(-10, -2) == 5


def test_divide_by_zero_raises_error():
    with pytest.raises(ValueError):
        divide_numbers(5, 0)