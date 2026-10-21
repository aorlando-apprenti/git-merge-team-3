# test_app.py
from app import multiply_numbers



def test_multiply_numbers():
    assert multiply_numbers(4, 3) == 12
    assert multiply_numbers(-2, 3) == -6
    assert multiply_numbers(5, 0) == 0
    assert multiply_numbers(1000000, 2) == 2000000