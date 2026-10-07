"""Shared statistical policy; validate before pandas aggregates."""
from math import isfinite
import pandas as pd
from calculator.validation import numeric_values


def mean(values):
    numbers = numeric_values(values)
    if len(numbers) < 1:
        raise ValueError("Mean requires at least one value.")
    return float(pd.Series(numbers, dtype=float).mean())


def standard_deviation(values, ddof=1):
    if ddof not in (0, 1):
        raise ValueError("ddof must be 0 (population) or 1 (sample).")
    numbers = numeric_values(values)
    if len(numbers) < 2:
        raise ValueError("Standard deviation requires at least two values.")
    result = float(pd.Series(numbers, dtype=float).std(ddof=int(ddof)))
    if not isfinite(result):
        raise ValueError("Result is outside the supported range.")
    return result