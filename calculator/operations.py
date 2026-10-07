"""Static math: no instance state, no I/O."""
from math import pow as _pow, sqrt as _sqrt
from calculator import statistics


class Operations:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        return a / b

    @staticmethod
    def square(value):
        return value * value

    @staticmethod
    def sqrt(value):
        if value < 0:
            raise ValueError("Cannot take the square root of a negative number.")
        return _sqrt(value)

    @staticmethod
    def power(value, *, exponent=2):
        return _pow(value, exponent)

    @staticmethod
    def sum(*values):
        if not values:
            raise ValueError("Enter at least one value.")
        total = 0.0
        for value in values:
            total += value
        return total

    @staticmethod
    def mean(*values):
        return statistics.mean(values)

    @staticmethod
    def stddev(*values, ddof=1):
        return statistics.standard_deviation(values, ddof=ddof)