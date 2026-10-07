import runpy
import pytest
from calculator.factory import CalculationFactory
from calculator.session import CalculatorSession
from calculator.commands import (Command, CalculateCommand, HistoryCommand,
                                 ClearHistoryCommand, HelpCommand)
from calculator.cli import prepare_command


def test_session_records_only_successes():
    session = CalculatorSession()
    assert session.calculate(CalculationFactory.create("add", 2, 3)) == 5.0
    with pytest.raises(ZeroDivisionError):
        session.calculate(CalculationFactory.create("divide", 1, 0))
    assert len(session.get_history()) == 1


def test_session_history_copy_and_independence():
    first, second = CalculatorSession(), CalculatorSession()
    first.calculate(CalculationFactory.create("add", 2, 3))
    first.get_history().clear()
    assert len(first.get_history()) == 1
    assert second.get_history() == []


def test_commands_return_display_text():
    session = CalculatorSession()
    calc = CalculationFactory.create("add", 2, 3)
    assert CalculateCommand(session, calc).execute() == "Result: 5.0000"
    assert HistoryCommand(session).execute() == "add 2.0 3.0 = 5.0000"
    assert ClearHistoryCommand(session).execute() == "History cleared."
    assert HistoryCommand(session).execute() == "History is empty."
    assert "add" in HelpCommand().execute()


def test_history_shows_saved_options():
    session = CalculatorSession()
    CalculateCommand(session, CalculationFactory.create("power", 3, exponent=4)).execute()
    assert HistoryCommand(session).execute() == "power 3.0 exponent=4.0 = 81.0000"


def test_incomplete_command_cannot_be_instantiated():
    class Incomplete(Command):
        pass

    with pytest.raises(TypeError):
        Incomplete()


def test_prepare_command_routes_and_rejects():
    session = CalculatorSession()
    assert isinstance(prepare_command("history", session), HistoryCommand)
    assert isinstance(prepare_command("clear", session), ClearHistoryCommand)
    assert isinstance(prepare_command("help", session), HelpCommand)
    for bad in ("", "history 1", "help me",
                "power 3 exponent=2 exponent=3", "power 3 =2"):
        with pytest.raises(ValueError):
            prepare_command(bad, session)


def test_loop_recovers_and_exits(run_cli):
    out = run_cli(["add 2 3", "divide 1 0", "bogus 1", "add 1 1", "history", "exit"])
    assert "Result: 5.0000" in out
    assert out.count("Error:") == 2
    assert "Result: 2.0000" in out           # success after failures
    assert out.strip().endswith("Goodbye!")


def test_eof_and_ctrl_c_exit_cleanly(run_cli):
    assert "Goodbye!" in run_cli([])
    assert "Goodbye!" in run_cli([KeyboardInterrupt()])


def test_module_entry_point(monkeypatch, capsys):
    def eof(prompt=""):
        raise EOFError

    monkeypatch.setattr("builtins.input", eof)
    runpy.run_module("calculator", run_name="__main__")
    assert "Goodbye!" in capsys.readouterr().out