import runpy
import pytest
from calculator.cli import run


def run_session(monkeypatch, capsys, inputs):
    input_iter = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(input_iter))
    run()
    return capsys.readouterr().out


def test_cli_add_and_exit(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["add", "10", "5", "exit"])
    assert "Result: 15" in out
    assert "goodbye!" in out


def test_cli_subtract_and_history(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["subtract", "20", "7", "history", "exit"])
    assert "Result: 13" in out
    assert "1: subtract 20 and 7 = 13" in out


def test_cli_remove_flow(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["add", "2", "3", "remove", "1", "history", "exit"])
    assert "Removed: Add" in out
    assert "History is empty." in out


def test_cli_empty_command_line(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["", "   ", "exit"])
    assert "goodbye!" in out


def test_cli_invalid_first_operand(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["add", "hello", "add", "4", "5", "exit"])
    assert "Invalid input: operands must be numbers." in out
    assert "Result: 9" in out


def test_cli_invalid_second_operand(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["add", "10", "invalid_b", "exit"])
    assert "Invalid input: operands must be numbers." in out


def test_cli_non_finite_first_operand(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["add", "nan", "5", "exit"])
    assert "Operands must be finite numbers." in out


def test_cli_non_finite_second_operand(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["add", "5", "inf", "exit"])
    assert "Operands must be finite numbers." in out


def test_cli_overflow_result(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["subtract", "-1e308", "1e308", "exit"])
    assert "Result overflowed." in out


def test_cli_help(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["help", "exit"])
    assert "Available commands: add, subtract, multiply, divide, history, remove, help, exit" in out


def test_cli_unknown_command(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["foobar", "exit"])
    assert "Unknown command: 'foobar'" in out


def test_cli_interrupt_keyboard(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt="": (_ for _ in ()).throw(KeyboardInterrupt))
    run()
    assert "goodbye!" in capsys.readouterr().out


def test_cli_interrupt_eof(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt="": (_ for _ in ()).throw(EOFError))
    run()
    assert "goodbye!" in capsys.readouterr().out


def test_main_module_execution(monkeypatch):
    input_iter = iter(["exit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(input_iter))
    runpy.run_module("calculator", run_name="__main__")


def test_main_imported_does_not_run():
    import importlib
    import calculator.__main__
    importlib.reload(calculator.__main__)


def test_cli_multiply(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["multiply", "6", "7", "exit"])
    assert "Result: 42" in out


def test_cli_divide(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["divide", "20", "4", "exit"])
    assert "Result: 5" in out


def test_cli_divide_by_zero_recovers(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["divide", "10", "0", "exit"])
    assert "Error: Cannot divide by zero." in out


# Stage 4 Independent Test
def test_stage4_independent_whitespace_case(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["  AdD  ", "30", "12", "exit"])
    assert "Result: 42" in out


# Stage 5 Independent Test
def test_stage5_independent_repeated_invalid_removal(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, [
        "add", "10", "10",
        "remove", "not_a_num",
        "remove", "99",
        "remove", "1",
        "history",
        "exit"
    ])
    assert "Invalid removal index." in out
    assert "Removed: Add" in out
    assert "History is empty." in out