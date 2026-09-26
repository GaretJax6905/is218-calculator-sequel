# Object-Oriented Calculator

An interactive, reliable command-line calculator demonstrating core Object-Oriented Programming (OOP) principles in Python: abstraction, encapsulation, inheritance, polymorphism, and comprehensive test coverage.

## Installation

1. Clone the repository:
```bash
   git clone https://github.com/GaretJax6905/is218_calculator.git
   cd is218_calculator
```

2. Create and activate a virtual environment:
```bash
   python3 -m venv .venv
   source .venv/bin/activate
```

3. Install dependencies:
```bash
   python -m pip install -r requirements.txt
```

## Running the Calculator

Start an interactive session:
```bash
python -m calculator
```

Available commands:

| Command    | Behavior                                                        |
|------------|------------------------------------------------------------------|
| `add`      | Adds two numbers and saves an `Add` object to history            |
| `subtract` | Subtracts two numbers and saves a `Subtract` object to history    |
| `multiply` | Multiplies two numbers and saves a `Multiply` object to history   |
| `divide`   | Divides two numbers and saves a `Divide` object to history        |
| `history`  | Displays operation names, operands, and results, numbered from 1  |
| `remove`   | Removes a displayed entry by index and renumbers the remaining ones |
| `help`     | Lists the available commands                                      |
| `exit`     | Ends the session cleanly                                           |

The calculator validates every operand and result: non-numeric input, non-finite values (NaN/infinity), division by zero, and out-of-range or non-numeric removal indices are all caught and reported without crashing the session or corrupting history. Pressing Ctrl+C or reaching end-of-input also exits cleanly.

History is kept in memory only for the current session and is cleared when the program exits.

## Running the Tests

Run the full test suite:
```bash
python -m pytest
```

This enforces 100% line and branch coverage, configured in `pytest.ini`. All tests must pass and coverage must be complete for the suite to succeed.

## Design Choices

- **Abstraction**: `calculation.py` defines an abstract `Calculation` base class (built on `abc.ABC`) with an abstract `get_result()` method. This gives every operation a shared contract instead of scattering arithmetic logic across unrelated code.
- **Inheritance & polymorphism**: `Add`, `Subtract`, `Multiply`, and `Divide` all inherit from `Calculation` and implement their own `get_result()`. The CLI's `OPERATIONS` dictionary maps command names to these classes, and code like `handle_history` calls `get_result()` polymorphically without ever checking which subclass it's holding.
- **Encapsulation**: `History` (in `history.py`) stores calculations in a private `_calculations` list. Callers only interact with it through `add()`, `get_history()` (which returns a defensive copy), and `remove()` — never by reaching into the list directly.
- **REPL**: `cli.py`'s `run()` function loops reading commands, dispatches them through a `COMMAND_HANDLERS` dictionary (for `exit`/`help`/`history`/`remove`) or `handle_operation()` (for the four arithmetic commands), and prints results until `exit` or an interrupt.
- **Error handling**: `validate_finite()` rejects NaN/infinite operands and results; `handle_operation()` catches `ValueError` and `ZeroDivisionError` around each calculation; `handle_remove()` catches `ValueError`/`IndexError` around removal. None of these propagate out and crash the session.

## Continuous Integration

GitHub Actions (`.github/workflows/tests.yml`) runs the full test suite with `pip install -r requirements.txt` and `python -m pytest`, across Python 3.11, 3.12, 3.13, and 3.14, on every push and pull request to `main`.

## Reflection: What Transfers to Another Language

To enforce that every operation must implement `get_result()` in Java or C#, you would define an `abstract class Calculation` containing an `abstract double getResult()` method, or define an `interface ICalculation` requiring that signature. Because both languages enforce contracts at compile time, any concrete subclass extending that abstract class or implementing the interface is forced by the compiler to provide the method implementation, or else the code will not compile. This concept is a staple in foundational statically typed OOP coursework (such as CS 113/114 or equivalent introductory Java/C# courses), where interfaces and abstract base classes establish structural contracts that downstream components rely on polymorphically.

Encapsulating state behind `add()`, `get_history()`, and `remove()` is a universal OOP design principle rather than a Python-specific trick, designed to protect internal invariants and prevent accidental corruption from outside code. By preventing direct access to `self._calculations`, the `History` class guarantees that only validated `Calculation` objects enter the collection, that deletions strictly adhere to 0-based boundary checks rather than silent negative index wrapping, and that callers only receive shallow copies so they cannot mutate or clear the internal list from outside. This exact pattern exists across virtually every object-oriented language, where languages like Java and C# enforce it even more strictly through the `private` access modifier and unmodifiable collection wrappers like `Collections.unmodifiableList()` or `IReadOnlyList<T>`.

While Python treats classes as first-class objects that can be stored in a dictionary lookup table, other languages typically handle name-to-behavior dispatching using design patterns or structured control flow. In languages like Java or C#, developers commonly employ the Factory Pattern via a dedicated `CalculationFactory` class that inspects the command string and instantiates the appropriate concrete subclass, often paired with modern switch expressions or pattern matching (such as C#'s `switch` expressions). Alternatively, statically typed environments can use reflection to dynamically load classes by name at runtime, though explicit factories, switch blocks, and map-based registries are preferred because they preserve type safety and performance without relying on reflection overhead.

The primary difference between Python's error handling and Java's is that Python uses unchecked exceptions exclusively, whereas Java divides exceptions into checked and unchecked categories. In Python, neither the runtime nor the interpreter requires functions to declare or callers to catch `ValueError` or `ZeroDivisionError`, allowing any unhandled exception to bubble up dynamically until caught or terminating the script. In contrast, while Java treats parsing failures (`NumberFormatException`) and standard arithmetic errors as unchecked `RuntimeException` instances, any custom domain error inheriting from `Exception` is considered a checked exception; Java forces methods to explicitly declare these in their method signatures using `throws` and refuses to compile unless calling code wraps the invocation in a `try/catch` block or propagates the declaration up the call stack. Additionally, standard floating-point division by zero in Java yields `Infinity` or `NaN` rather than throwing an exception like Python's `ZeroDivisionError`, requiring explicit pre-checks if zero division must be handled as an exceptional event.