import gradio as gr
import pytest

from app import add, calculate, divide, multiply, square, subtract


def test_add_function():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract_function():
    assert subtract(5, 3) == 2
    assert subtract(1, 1) == 0


def test_multiply_function():
    assert multiply(2, 3) == 6
    assert multiply(-1, 5) == -5


def test_divide_function():
    assert divide(6, 2) == 3
    assert divide(-10, 2) == -5
    assert divide(0, 5) == 0
    with pytest.raises(gr.Error):
        divide(5, 0)


def test_square_function():
    assert square(3) == 9
    assert square(-3) == 9


def test_calculate_function():
    assert calculate("Add", 2, 3) == 5
    assert calculate("Subtract", 5, 2) == 3
    assert calculate("Multiply", 4, 3) == 12
    assert calculate("Divide", 8, 2) == 4
    assert calculate("Square", 5, 999) == 25
    with pytest.raises(gr.Error):
        calculate("Divide", 5, 0)
