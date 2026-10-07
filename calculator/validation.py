"""Convert inputs to finite floats; raise so callers choose the response."""
from math import isfinite


def numeric_values(values):
    numbers = []
    for value in values:
        try:
            number = float(value)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid number: {value}") from None
        if not isfinite(number):
            raise ValueError(f"Number must be finite: {value}")
        numbers.append(number)
    return tuple(numbers)