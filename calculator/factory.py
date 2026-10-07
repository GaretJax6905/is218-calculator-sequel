"""A factory centralizes construction; it does not execute math."""
from calculator.calculation import Calculation
from calculator.operations import Operations


class CalculationFactory:
    operations = {
        "add": Operations.add,
        "subtract": Operations.subtract,
        "multiply": Operations.multiply,
        "divide": Operations.divide,
    }

    @staticmethod
    def create(name, a, b):
        name = name.strip().lower()
        try:
            operation = CalculationFactory.operations[name]
        except KeyError:
            raise ValueError(f"Unknown operation: {name}") from None
        return Calculation(a, b, operation)