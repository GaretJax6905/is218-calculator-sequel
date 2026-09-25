import pytest
from calculator.calculation import Add


def test_add_positive():
    calc = Add(10, 5)
    assert calc.get_result() == 15


def test_add_negative():
    calc = Add(-10, -5)
    assert calc.get_result() == -15


def test_add_mixed():
    calc = Add(10, -5)
    assert calc.get_result() == 5


def test_add_zero():
    calc = Add(0, 0)
    assert calc.get_result() == 0


# Stage 1 Independent Test:
def test_operands_remain_unchanged():
    calc = Add(14, -6)
    assert calc.get_result() == 8
    assert calc.a == 14
    assert calc.b == -6