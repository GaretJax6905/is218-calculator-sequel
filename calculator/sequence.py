"""Process already prepared calculations independently."""


def execute_sequence(session, calculations):
    results = []
    errors = []
    for calculation in calculations:
        try:
            result = session.calculate(calculation)
        except (ValueError, ZeroDivisionError, OverflowError) as error:
            errors.append(str(error))
        else:
            results.append(result)
    return results, errors