# test_app.py
import pytest
from app import multiply_numbers
from app import add_numbers
from app import subtract_numbers
from app import divide_numbers

def test_multiply_numbers():
    assert multiply_numbers(4, 3) == 12
    assert multiply_numbers(-2, 3) == -6
    assert multiply_numbers(5, 0) == 0
    assert multiply_numbers(1000000, 2) == 2000000


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


def test_subtract_numbers():
    assert subtract_numbers(5, 3) == 2
    assert subtract_numbers(3, 5) == -2
    assert subtract_numbers(0, 0) == 0
    assert subtract_numbers(-4, -2) == -2
