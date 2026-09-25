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


def test_cli_invalid_operand_recovers(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["add", "hello", "add", "4", "5", "exit"])
    assert "Invalid input" in out
    assert "Result: 9" in out


def test_cli_non_finite_input(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["add", "nan", "5", "exit"])
    assert "Operands must be finite numbers." in out


def test_cli_help(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["help", "exit"])
    assert "Available commands" in out


def test_cli_unknown_command(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["unknown", "exit"])
    assert "Unknown command" in out


def test_cli_interrupt(monkeypatch, capsys):
    def raise_interrupt(prompt=""):
        raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", raise_interrupt)
    run()
    captured = capsys.readouterr().out
    assert "goodbye!" in captured


def test_main_entry_module(monkeypatch):
    input_iter = iter(["exit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(input_iter))
    runpy.run_module("calculator", run_name="__main__")


# Stage 4 Independent Test:
def test_stage4_independent_whitespace_case(monkeypatch, capsys):
    out = run_session(monkeypatch, capsys, ["  AdD  ", "30", "12", "exit"])
    assert "Result: 42" in out


# Stage 5 Independent Test:
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