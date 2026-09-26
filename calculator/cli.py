import math
from typing import Callable, Dict, NoReturn
from calculator.calculation import Add, Subtract, Multiply, Divide
from calculator.history import History

OPERATIONS = {
    "add": Add,
    "subtract": Subtract,
    "multiply": Multiply,
    "divide": Divide,
}


def format_number(val: float) -> str:
    return f"{val:g}"


def validate_finite(val: float, message: str) -> None:
    math.isfinite(val) or (_ for _ in ()).throw(ValueError(message))


def handle_exit(history: History) -> NoReturn:
    print("goodbye!")
    raise SystemExit


def handle_help(history: History) -> None:
    print("Available commands: add, subtract, multiply, divide, history, remove, help, exit")


def handle_history(history: History) -> None:
    items = history.get_history()
    output = "\n".join(
        f"{idx}: {item.__class__.__name__.lower()} {format_number(item.a)} and "
        f"{format_number(item.b)} = {format_number(item.get_result())}"
        for idx, item in enumerate(items, start=1)
    )
    print(output or "History is empty.")


def handle_remove(history: History) -> None:
    try:
        idx = int(input("Enter index to remove: ").strip()) - 1
        removed = history.remove(idx)
        print(f"Removed: {removed.__class__.__name__} ({format_number(removed.a)}, {format_number(removed.b)})")
    except (ValueError, IndexError):
        print("Invalid removal index.")


def handle_operation(command: str, history: History) -> None:
    try:
        a = float(input("Enter first number: ").strip())
        validate_finite(a, "Operands must be finite numbers.")
        b = float(input("Enter second number: ").strip())
        validate_finite(b, "Operands must be finite numbers.")

        calc = OPERATIONS[command](a, b)
        result = calc.get_result()
        validate_finite(result, "Result overflowed.")

        history.add(calc)
        print(f"Result: {format_number(result)}")
    except ValueError as exc:
        msg = str(exc)
        print(msg if msg in ("Operands must be finite numbers.", "Result overflowed.") else "Invalid input: operands must be numbers.")
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")


COMMAND_HANDLERS: Dict[str, Callable[[History], None]] = {
    "exit": handle_exit,
    "help": handle_help,
    "history": handle_history,
    "remove": handle_remove,
}


def run() -> None:
    history = History()

    while True:
        try:
            raw_command = input("Enter command: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\ngoodbye!")
            break

        command = raw_command.lower()
        action = COMMAND_HANDLERS.get(
            command,
            lambda h, cmd=command: handle_operation(cmd, h)
            if cmd in OPERATIONS
            else print(f"Unknown command: '{raw_command}'. Type 'help' for instructions.")
        )

        try:
            action(history)
        except SystemExit:
            break