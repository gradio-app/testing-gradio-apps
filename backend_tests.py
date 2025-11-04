import pytest
from app import add, subtract, multiply, divide, square, calculate

def test_add_function():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(10.5, 2.5) == 13.0

def test_subtract_function():
    assert subtract(5, 3) == 2
    assert subtract(1, 1) == 0
    assert subtract(0, 5) == -5
    assert subtract(10.5, 2.5) == 8.0

def test_multiply_function():
    assert multiply(2, 3) == 6
    assert multiply(-1, 5) == -5
    assert multiply(0, 100) == 0
    assert multiply(2.5, 4) == 10.0

def test_divide_function():
    assert divide(6, 2) == 3
    assert divide(5, 2) == 2.5
    assert divide(-10, 2) == -5
    assert divide(0, 5) == 0
    assert divide(5, 0) == "Error: Division by zero"

def test_square_function():
    assert square(3) == 9
    assert square(-3) == 9
    assert square(0) == 0
    assert square(2.5) == 6.25
    assert square(4, 999) == 16  # Second parameter should be ignored

def test_calculate_function():
    assert calculate("Add", 2, 3) == 5
    assert calculate("Subtract", 5, 2) == 3
    assert calculate("Multiply", 4, 3) == 12
    assert calculate("Divide", 8, 2) == 4
    assert calculate("Square", 5, 999) == 25
    assert calculate("Unknown", 1, 2) == "Error: Unknown operation"
    
def test_calculate_edge_cases():
    assert calculate("Divide", 5, 0) == "Error: Division by zero"
    assert calculate("Add", 0, 0) == 0