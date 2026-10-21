# app.py
def multiply_numbers(a: int, b: int) -> int:
    return a * b

    
def add_numbers(a: int, b: int) -> int:
    return a + b


def divide_numbers(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def subtract_numbers(a: int, b: int) -> int:
    return a - b
