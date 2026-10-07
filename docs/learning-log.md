# Learning Log — Calculator Sequel

## 1. From subclasses to callable composition

My original calculator used inheritance: `Add`, `Subtract`, `Multiply`, and `Divide` each subclassed an abstract `Calculation` and overrode `get_result()`. The only real difference between those subclasses was one line of arithmetic, so every new operation meant a new class.

In the sequel, the arithmetic lives in static methods on `Operations`, and a single `Calculation` class stores the operation as a callable:

```python
calculation = Calculation([2, 3], Operations.add)
calculation.get_result()   # calls Operations.add(2.0, 3.0)
```

The relationship changed from "Add **is a** Calculation" to "Calculation **has an** operation." Adding a new operation now means writing one static method and registering it in the factory, not creating a subclass. The tradeoff is that a plain callable has no compiler- or ABC-enforced contract the way an abstract subclass does; the factory registry and tests are what keep the set of operations correct.

Inheritance is still the right tool for application commands. `CalculateCommand`, `HistoryCommand`, `ClearHistoryCommand`, `CountCommand`, and `HelpCommand` do genuinely different work, not just a different formula, and they need different state (most hold a session; help holds nothing). The abstract `Command` class with `@abstractmethod execute()` guarantees every action can be invoked the same way by the CLI. My test `test_incomplete_command_cannot_be_instantiated` shows the ABC refusing a subclass that forgets `execute()`.

## 2. Python concepts

**Static vs. instance methods.** `Operations.add` is a `@staticmethod`: Python doesn't pass an instance, so it can be called as `Operations.add(2, 3)` without constructing anything. That fits because the math needs nothing except its arguments. `Calculation.get_result()` and `Command.execute()` are instance methods because they depend on state stored on the object: the saved values, options, callable, or session. "Static" describes how the method is bound; it doesn't mean faster or automatically pure.

**Callable vs. call.** `operation = Operations.add` stores behavior; `operation(2, 3)` runs it. The parentheses are the difference. The factory registry stores callables without parentheses, so selecting an operation never performs math.

**Operands vs. named settings.** Operands are the data being calculated on (`3` in `power 3`). Settings configure how the operation behaves (`exponent=4`, `ddof=0`). In `Operations` the settings are keyword-only, using a bare `*` in the signature, so `power(3, 4)` is rejected and the caller has to write `power(3, exponent=4)`. That makes configuration explicit and impossible to confuse with an operand.

**Gathering vs. unpacking.** The same symbols do opposite jobs depending on where they appear:

| Location | `*` | `**` |
|---|---|---|
| In a signature: `def create(name, *values, **options)` | gathers extra positional args into a tuple | gathers named args into a dict |
| At a call: `self.operation(*self.values, **self.options)` | unpacks a sequence into positional args | unpacks a dict into named args |

The CLI calls `CalculationFactory.create(name, *values, **options)` (unpacking), the factory signature gathers them back, and `get_result()` unpacks them again into the operation.

## 3. Factory construction vs. command execution

The factory's job is to **build** a calculation: normalize the name, pick the callable, enforce operand count and allowed options, convert settings to finite floats, and return an unexecuted `Calculation`. A command's job is to **perform an application action** and return display text. The session is the receiver that commands act on, and the CLI is the invoker. A factory isn't a command just because it creates objects.

### Success trace: `power 3 exponent=4`

1. **CLI input.** `run()` reads `"power 3 exponent=4"` and calls `prepare_command`.
2. **Parsing.** The text is split into `name="power"`, `values=["3"]` (strings), and `options={"exponent": "4"}` (string).
3. **Construction.** `CalculationFactory.create("power", "3", exponent="4")`:
   - normalizes the name and selects `Operations.power`
   - checks that `exponent` is allowed for power and converts it to `4.0`
   - checks the operand count is exactly 1
   - builds `Calculation(("3",), Operations.power, exponent=4.0)`, whose constructor converts the values to `(3.0,)`

   **No math has run yet.**
4. **Wrapping.** `prepare_command` returns `CalculateCommand(session, calculation)`.
5. **Execution.** `command.execute()` calls `session.calculate(calculation)`, which calls `calculation.get_result()`, which calls `Operations.power(3.0, exponent=4.0)` and returns `81.0`. `get_result()` confirms the result is finite.
6. **Recording.** Only after success, `History.add(calculation, 81.0)` saves the pair.
7. **Display.** `execute()` returns `"Result: 81.0000"` and the CLI prints it. `history` later shows `power 3.0 exponent=4.0 = 81.0000` from the saved result.

### Failure trace: `divide 1 0`

1. **Parsing.** `name="divide"`, `values=["1", "0"]`, and no options.
2. **Construction.** This succeeds. The factory checks the count (2), and `Calculation` converts the values to `(1.0, 0.0)`. Dividing by zero isn't detected at construction, because construction never runs math.
3. **Execution.** `execute()` calls `session.calculate()`, which calls `get_result()`, which calls `Operations.divide(1.0, 0.0)`. That raises **`ZeroDivisionError`**, which is where the exception originates.
4. **Propagation.** The exception passes up through `get_result()`, `session.calculate()`, and `execute()` without being caught. The line `self._history.add(calculation, result)` in the session is **skipped**, because control leaves before it runs.
5. **Handling.** The `except (ValueError, OSError, ZeroDivisionError, ...)` block in `cli.run()` catches it and prints `Error: float division by zero`.
6. **Recovery.** The `while True` loop continues and the next prompt appears. History is unchanged.

## 4. History ownership

`History` owns a private `_entries` list and only exposes `add`, `get_history`, and `clear`. Callers can't append bad entries or delete items directly, so the rule "only successful calculations are recorded" can be enforced in one place, `CalculatorSession.calculate`, instead of trusting every caller to do it correctly. The session doesn't expose a public mutable list either.

`get_history()` returns `list(self._entries)`, which is a **shallow copy**. It protects the *collection*: clearing or appending to the returned list doesn't change the session's history (`test_history_copy_protects_entries` and `test_session_history_copy_and_independence` prove this). Its limit is that the `Calculation` objects inside are still shared, so a caller could reassign an attribute on one of them. That's acceptable here because nothing in the app mutates calculations after construction, but it isn't a deep, immutable record.

Each entry saves `(calculation, result)` instead of recalculating for display. That keeps `history` cheap and stable, and it means displaying history can never raise a math error or produce a different answer than the one the user saw. Execution and recording stay separate responsibilities: `History.add` never calls `get_result()`.

## 5. EAFP / LBYL and statistics policy

I used **EAFP** (try it, handle the failure) where the operation itself already reports a precise error:
- **Factory name lookup:** `CalculationFactory.operations[name]` inside `try/except KeyError`, re-raised as `ValueError("Unknown operation")`. Only the lookup sits inside the `try`, so an unrelated error during construction isn't mislabeled as an unknown name.
- **Number conversion:** `float(value)` inside `try/except (TypeError, ValueError)` in `numeric_values`. Trying the conversion is the most reliable test of whether a string is a number.
- **File access:** I don't check whether a CSV exists before reading it. The file could disappear between the check and the read, so `pd.read_csv` is allowed to raise, and the CLI catches `OSError`/`EmptyDataError`.

I used **LBYL** (check first) for this application's own rules, which no library would enforce for me:
- **Operand counts** in the factory (`add` needs exactly 2).
- **Minimum observations:** sum and mean need at least one value; standard deviation needs at least two. Python's `sum([])` returns 0 and pandas can return NaN for one value, so I check explicitly, before aggregating, and raise a clear `ValueError`.
- **CSV header:** `if "value" not in frame.columns`.
- **ddof:** only 0 or 1 is accepted.

The choice is about correctness and clear error ownership, not speed.

**Sample vs. population.** Pandas divides by `n - ddof`. The default `ddof=1` gives the **sample** standard deviation (divide by n−1), and `ddof=0` gives the **population** deviation (divide by n). For 2, 4, 6 the squared deviations sum to 8, so the sample variance is 8/2 = 4 (std 2.0) and the population variance is 8/3 (std ≈ 1.6330). `test_mean_and_sample_vs_population` checks both. I validate every value as finite *before* pandas runs, because pandas would otherwise skip missing values silently and give an answer computed from fewer observations than the user supplied.

## 6. Independent adaptation: `count`

I added a `count` action that reports the number of successful calculations in the session.

- **commands.py:** a new `CountCommand(Command)` whose `execute()` returns `Successful calculations: N` using `len(session.get_history())`. The `HELP` text was also updated.
- **cli.py:** `"count": CountCommand` added to the `actions` dictionary, so it automatically follows the existing rule that actions take no arguments.
- **No changes** to `Operations`, `Calculation`, the factory, or `History`. Counting is an application action about session state, not math, so it belongs in commands, not in `Operations`.

`test_count_reports_only_successes` runs one success and one failed division, then asserts the count is 1. That proves the count reflects the session's success-only recording rule instead of every attempt. I also added `sequence.py` (Part 6B), which runs prepared calculations independently: each item has its own `try`, so a failure in the middle doesn't stop later items, and only successes reach history (`test_sequence_continues_after_failure`: results `[5.0, 9.0]`, one error, two history entries).

## 7. Test changes and what the tests establish

**Removed tests.** My original `test_calculation.py`, `test_cli.py`, and `test_history.py` targeted APIs that were intentionally removed: the `Add`/`Subtract` subclasses, the `remove` command, and the old dispatch-dictionary CLI. Individual removal is not a requirement of this extension, and the calculation interface changed from subclasses to `Calculation(values, operation, **options)`. The behavior those tests protected is now covered by the new suite:

| Original behavior | Now covered by |
|---|---|
| Arithmetic results, divide by zero | `test_arithmetic`, `test_divide_by_zero_raises` |
| Rejecting nonnumeric/NaN/infinite input | `test_numeric_values_converts_and_rejects` |
| Rejecting nonfinite results | `test_nonfinite_result_rejected` |
| History returns a defensive copy | `test_history_copy_protects_entries` |
| CLI recovers from errors, exits on EOF/Ctrl+C | `test_loop_recovers_and_exits`, `test_eof_and_ctrl_c_exit_cleanly` |

**What the key tests prove, and why those cases matter:**
- `test_construction_does_not_execute` uses a spy callable that records each call. The list is empty after construction and holds exactly one call after `get_result()`. This proves *when* math runs, which a numeric assertion alone can't show.
- `test_factory_does_not_execute` builds `divide 1 0` without error, then fails on execution. Construction and execution are separate steps.
- `test_session_records_only_successes` covers a success, then a failure, then a history length of 1. Failed calculations never pollute history.
- `test_loop_recovers_and_exits` asserts a *later* success (`add 1 1`) after two errors. Recovery means the session keeps working, not just that an error message printed.
- `test_power_exponent_is_keyword_only` checks that `power(3, 4)` raises `TypeError`, so the keyword-only contract is enforced.
- `test_csv_matches_typed_input` compares `csv mean`/`csv stddev` on a temp file to typed input on the same data. Different sources go through the same policy. It uses `tmp_path` so the supplied `values.csv` is never modified.
- `test_csv_structure_and_missing_values` covers a wrong header and a quoted empty cell. Bad observations are rejected, not silently dropped.
- `test_failed_file_then_manual_success` covers a missing file and an empty file, then a successful typed `mean`. File errors don't break the session.

`pytest.ini` enforces 100% line and branch coverage, and CI runs the suite on Python 3.11–3.14. Coverage shows every line *ran*, not that every requirement is correct. The tests above are what establish the specific claims.

## Sources and reuse

- Structure and several components (`numeric_values`, the factory's registry/option loop, `session.py`, `commands.py`, the CLI parser, `inputs.py`) follow the course reference branches in `kaw393939/is218-command-factory-statistics`, Parts 1–6.
- The starting point was my earlier repo, `GaretJax6905/is218_calculator`. Its private-list `History` with a defensive copy carried forward conceptually.
