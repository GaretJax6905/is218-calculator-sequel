import math
from calculator.calculation import Add, Subtract
from calculator.history import History

OPERATIONS = {
    "add": Add,
    "subtract": Subtract,
}


def format_number(val: float) -> str:
    return f"{val:g}"


def run() -> None:
    history = History()

    while True:
        try:
            raw_command = input("Enter command: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\ngoodbye!")
            break

        if not raw_command:
            continue

        command = raw_command.lower()

        if command == "exit":
            print("goodbye!")
            break
        elif command == "help":
            print("Available commands: add, subtract, history, remove, help, exit")
        elif command == "history":
            items = history.get_history()
            if not items:
                print("History is empty.")
            else:
                for idx, item in enumerate(items, start=1):
                    op_name = item.__class__.__name__.lower()
                    print(f"{idx}: {op_name} {format_number(item.a)} and {format_number(item.b)} = {format_number(item.get_result())}")
        elif command == "remove":
            try:
                idx_input = input("Enter index to remove: ").strip()
                idx = int(idx_input) - 1
                removed = history.remove(idx)
                print(f"Removed: {removed.__class__.__name__} ({format_number(removed.a)}, {format_number(removed.b)})")
            except (ValueError, IndexError):
                print("Invalid removal index.")
        elif command in OPERATIONS:
            try:
                a_str = input("Enter first number: ").strip()
                a = float(a_str)
                b_str = input("Enter second number: ").strip()
                b = float(b_str)

                if not (math.isfinite(a) and math.isfinite(b)):
                    print("Operands must be finite numbers.")
                    continue

                calc_class = OPERATIONS[command]
                calculation = calc_class(a, b)
                result = calculation.get_result()

                if not math.isfinite(result):
                    print("Result overflowed.")
                    continue

                history.add(calculation)
                print(f"Result: {format_number(result)}")
            except ValueError:
                print("Invalid input: operands must be numbers.")
        else:
            print(f"Unknown command: '{raw_command}'. Type 'help' for instructions.")