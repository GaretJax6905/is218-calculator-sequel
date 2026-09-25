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

from calculator.calculation import Calculation, Subtract


def test_subtract_positive():
    calc = Subtract(20, 7)
    assert calc.get_result() == 13


def test_subtract_negative():
    calc = Subtract(-10, -5)
    assert calc.get_result() == -5


def test_calculation_abstract_instantiation():
    with pytest.raises(TypeError):
        Calculation(10, 5)


def test_polymorphic_evaluation():
    calculations = [Add(10, 5), Subtract(20, 7)]
    results = [c.get_result() for c in calculations]
    assert results == [15, 13]


# Stage 2 Independent Test:
def test_polymorphic_loop_independent():
    calcs = [Add(4.0, 2.0), Subtract(5.0, 12.0), Add(-3.0, 1.0)]
    results = [c.get_result() for c in calcs]
    assert results == [6.0, -7.0, -2.0]