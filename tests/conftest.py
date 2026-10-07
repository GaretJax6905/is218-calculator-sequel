import pytest
from calculator.cli import run


@pytest.fixture
def run_cli(monkeypatch, capsys):
    def _run(inputs):
        feed = iter(inputs)

        def fake_input(prompt=""):
            try:
                value = next(feed)
            except StopIteration:
                raise EOFError
            if isinstance(value, BaseException):
                raise value
            return value

        monkeypatch.setattr("builtins.input", fake_input)
        run()
        return capsys.readouterr().out
    return _run