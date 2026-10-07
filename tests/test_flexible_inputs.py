import pytest
from calculator.factory import CalculationFactory
from calculator.operations import Operations


def test_unary_and_collection_operations():
    assert Operations.square(3) == 9
    assert Operations.sqrt(9) == 3
    assert Operations.power(3) == 9                 # default exponent
    assert Operations.power(3, exponent=4) == 81
    assert Operations.sum(2, 3, 4) == 9


def test_power_exponent_is_keyword_only():
    with pytest.raises(TypeError):
        Operations.power(3, 4)


def test_sum_requires_a_value():
    with pytest.raises(ValueError):
        Operations.sum()


def test_sum_accepts_any_count_through_factory():
    assert CalculationFactory.create("sum", 1, 2, 3, 4).get_result() == 10.0


def test_negative_sqrt_fails_at_execution_not_construction():
    calc = CalculationFactory.create("sqrt", -4)
    with pytest.raises(ValueError):
        calc.get_result()


def test_options_are_converted():
    calc = CalculationFactory.create("power", "3", exponent="4")
    assert calc.options == {"exponent": 4.0}
    assert calc.get_result() == 81.0


def test_wrong_operand_counts():
    with pytest.raises(ValueError):
        CalculationFactory.create("add", 1)
    with pytest.raises(ValueError):
        CalculationFactory.create("square", 1, 2)


def test_unsupported_and_nonfinite_options():
    with pytest.raises(ValueError):
        CalculationFactory.create("add", 1, 2, exponent=2)
    with pytest.raises(ValueError):
        CalculationFactory.create("power", 2, exponent="nan")