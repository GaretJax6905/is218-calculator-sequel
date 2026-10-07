from calculator.factory import CalculationFactory

print(CalculationFactory.create("add", 2, 3).get_result())
print(CalculationFactory.create("power", 3, exponent=4).get_result())