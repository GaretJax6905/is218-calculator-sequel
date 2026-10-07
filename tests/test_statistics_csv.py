import pytest
from calculator.operations import Operations
from calculator.session import CalculatorSession
from calculator.cli import prepare_command
from calculator.inputs import read_csv_values


def test_mean_and_sample_vs_population():
    assert Operations.mean(2, 4, 6) == 4.0
    assert Operations.stddev(2, 4, 6) == 2.0                       # sample, n-1
    assert Operations.stddev(2, 4, 6, ddof=0) == pytest.approx(1.6330, abs=1e-4)


def test_statistical_minimums_and_policy():
    with pytest.raises(ValueError):
        Operations.mean()
    with pytest.raises(ValueError):
        Operations.stddev(5)
    with pytest.raises(ValueError):
        Operations.stddev(1, 2, ddof=2)
    with pytest.raises(ValueError):
        Operations.stddev(1e308, -1e308)                           # overflow


def test_csv_matches_typed_input(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("value\n2\n4\n6\n")
    session = CalculatorSession()
    for op in ("mean", "stddev"):
        assert (prepare_command(f"csv {op} {path}", session).execute()
                == prepare_command(f"{op} 2 4 6", session).execute())


def test_csv_structure_and_missing_values(tmp_path):
    no_header = tmp_path / "other.csv"
    no_header.write_text("reading\n1\n2\n")
    with pytest.raises(ValueError):
        read_csv_values(no_header)
    missing = tmp_path / "missing.csv"
    missing.write_text('value\n1\n""\n3\n')                        # not silently dropped
    with pytest.raises(ValueError):
        prepare_command(f"csv mean {missing}", CalculatorSession())


def test_csv_usage_errors():
    session = CalculatorSession()
    with pytest.raises(ValueError):
        prepare_command("csv mean", session)
    with pytest.raises(ValueError):
        prepare_command("csv add values.csv", session)


def test_failed_file_then_manual_success(tmp_path, run_cli):
    empty = tmp_path / "empty.csv"
    empty.write_text("")
    out = run_cli(["csv mean nope.csv", f"csv mean {empty}", "mean 1 2 3", "exit"])
    assert out.count("Error:") == 2
    assert "Result: 2.0000" in out