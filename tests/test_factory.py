import pytest
from calculator.factory import CalculationFactory
from calculator.operations import Operations


def test_factory_normalizes_and_builds():
    calc = CalculationFactory.create(" ADD ", "2", "3")
    assert calc.operation is Operations.add
    assert calc.get_result() == 5.0


def test_unknown_name():
    with pytest.raises(ValueError, match="Unknown operation"):
        CalculationFactory.create("modulo", 1, 2)


def test_factory_does_not_execute():
    calc = CalculationFactory.create("divide", 1, 0)   # no error yet
    with pytest.raises(ZeroDivisionError):
        calc.get_result()