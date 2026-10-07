from calculator.factory import CalculationFactory

print(CalculationFactory.create(" ADD ", "2", "3").get_result())