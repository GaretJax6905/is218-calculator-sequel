from abc import ABC, abstractmethod


class Calculation(ABC):
    def __init__(self, a: float, b: float) -> None:
        self.a: float = a
        self.b: float = b

    @abstractmethod
    def get_result(self) -> float:
        """Calculate and return the result."""


class Add(Calculation):
    def get_result(self) -> float:
        return self.a + self.b


class Subtract(Calculation):
    def get_result(self) -> float:
        return self.a - self.b


class Multiply(Calculation):
    def get_result(self) -> float:
        return self.a * self.b


class Divide(Calculation):
    def get_result(self) -> float:
        return self.a / self.b if self.b != 0 else (_ for _ in ()).throw(ZeroDivisionError("Cannot divide by zero."))