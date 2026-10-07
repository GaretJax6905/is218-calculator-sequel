"""Parse one line into a command, invoke it, print, repeat."""
from calculator.commands import (CalculateCommand, ClearHistoryCommand,
                                 HelpCommand, HistoryCommand)
from calculator.factory import CalculationFactory
from calculator.session import CalculatorSession


def prepare_command(text, session):
    parts = text.split()
    if not parts:
        raise ValueError("Enter a command; use help for examples.")
    name, *arguments = parts
    name = name.lower()
    actions = {"history": HistoryCommand, "clear": ClearHistoryCommand}
    if name in actions:
        if arguments:
            raise ValueError(f"{name} does not accept values.")
        return actions[name](session)
    if name == "help":
        if arguments:
            raise ValueError("help does not accept values.")
        return HelpCommand()
    values = []
    options = {}
    for argument in arguments:
        if "=" in argument:
            key, value = argument.split("=", 1)
            if not key or key in options:
                raise ValueError("Options need unique names: key=value.")
            options[key] = value
        else:
            values.append(argument)
    calculation = CalculationFactory.create(name, *values, **options)
    return CalculateCommand(session, calculation)


def run() -> None:
    session = CalculatorSession()
    print("Calculator")
    print(HelpCommand().execute())
    while True:
        try:
            text = input("> ").strip()
            if text.lower() == "exit":
                break
            command = prepare_command(text, session)
            print(command.execute())
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except (ValueError, ZeroDivisionError, OverflowError) as error:
            print(f"Error: {error}")
    print("Goodbye!")