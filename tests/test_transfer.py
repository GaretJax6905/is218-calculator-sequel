from calculator.factory import CalculationFactory
from calculator.session import CalculatorSession
from calculator.sequence import execute_sequence
from calculator.commands import CountCommand
from calculator.cli import prepare_command


def test_sequence_continues_after_failure():
    session = CalculatorSession()
    calcs = [CalculationFactory.create("add", 2, 3),
             CalculationFactory.create("divide", 1, 0),
             CalculationFactory.create("square", 3)]
    results, errors = execute_sequence(session, calcs)
    assert results == [5.0, 9.0]                 # later item still runs
    assert len(errors) == 1
    assert len(session.get_history()) == 2       # failure not recorded


def test_count_reports_only_successes():
    session = CalculatorSession()
    execute_sequence(session, [CalculationFactory.create("add", 1, 1),
                               CalculationFactory.create("divide", 1, 0)])
    assert CountCommand(session).execute() == "Successful calculations: 1"
    assert isinstance(prepare_command("count", session), CountCommand)