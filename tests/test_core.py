import runpy
import pytest
from calculator.operations import Operations
from calculator.calculation import Calculation
from calculator.history import History
from calculator.validation import numeric_values


def test_arithmetic():
    assert Operations.add(2, 3) == 5
    assert Operations.subtract(2, 3) == -1
    assert Operations.multiply(2, 3) == 6
    assert Operations.divide(7, 2) == 3.5


def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        Operations.divide(1, 0)


def test_numeric_values_converts_and_rejects():
    assert numeric_values(["2", 3]) == (2.0, 3.0)
    for bad in (["abc"], ["inf"], ["nan"], [None]):
        with pytest.raises(ValueError):
            numeric_values(bad)


def test_construction_does_not_execute():
    calls = []

    def spy(a, b):
        calls.append((a, b))
        return a + b

    calc = Calculation([2, 3], spy)
    assert calls == []                       # stored, not run
    assert calc.get_result() == 5.0
    assert calls == [(2.0, 3.0)]             # run exactly once


def test_zero_divisor_constructs_then_fails():
    calc = Calculation([1, 0], Operations.divide)
    with pytest.raises(ZeroDivisionError):
        calc.get_result()


def test_nonfinite_result_rejected():
    calc = Calculation([1e308, 10], Operations.multiply)
    with pytest.raises(ValueError):
        calc.get_result()


def test_history_copy_protects_entries():
    history = History()
    calc = Calculation([2, 3], Operations.add)
    history.add(calc, 5.0)
    history.get_history().clear()            # mutate the copy
    assert history.get_history() == [(calc, 5.0)]
    history.clear()
    assert history.get_history() == []


def test_demo_entry_point(capsys):
    runpy.run_module("calculator", run_name="__main__")
    assert "5.0" in capsys.readouterr().out