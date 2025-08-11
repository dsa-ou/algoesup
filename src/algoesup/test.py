"""Simplified testing for Python functions, see the [examples](coding.ipynb#testing)."""

from inspect import Parameter, signature
from typing import Callable

def check_table(test_table: list | tuple, types: list = [], min: int = 1, max: int = 0) -> list[str]:
    """Check the structure of `test_table` and return a list of error messages.

    This auxiliary function does the checks for `check_tests` and `test`:

    - the table is a list or tuple with at least `min` tests
    - the table has at most `max` tests (if `max` is greater than 0)
    - each test is a list or tuple with a string followed by one or more values
    - each input and output value has the expected type (if `types` is given).

    Args:
        test_table (list|tuple): The sequence of tests, each one a list or
            tuple with: a string (the test name); zero or more values (the inputs to the function);
            the expected output value.
        types (list): Expected types of the inputs and output.
            Set this argument only if the number and order of inputs are fixed.
        min (int): Minimum number of tests in the table. Default is 1.
        max (int): Maximum number of tests in the table. Default is 0 (no maximum).

    Returns:
        list[str]: The error messages. The list is empty if the table is well defined.
    """
    if min < 0 or max < 0:
        raise ValueError("Minimum and maximum number of tests must be >= 0.")
    if 0 < max < min:
        raise ValueError("Maximum number of tests must be >= minimum number.")
    if not isinstance(test_table, (list, tuple)):
        return ["the table must be a list or tuple"]
    messages = []
    for number, test in enumerate(test_table, start=1):
        if not isinstance(test, (list, tuple)):
            messages.append(f"test {number} must be a list or tuple")
        elif len(test) < 2:
            messages.append(f"test {number} must have two or more elements")
        elif not isinstance(test[0], str):
            messages.append(f"test {number} must have a string as first element")
        elif types:
            name = test[0]
            if len(types) != len(test) - 1:
                messages.append(f"test '{name}' must have {len(types)-1} input(s) and 1 output")
            for value, expected_type in zip(test[1:], types):
                if not isinstance(value, expected_type):
                    messages.append(f'in test "{name}", {value} must have type {expected_type.__name__}')
    n = len(test_table)
    if n < min:
        messages.append(f"the table must have at least {min} tests, but has {n}")
    elif n > max > 0:
        messages.append(f"the table can have at most {max} tests, but has {n}")
    return messages

def check_tests(test_table: list | tuple, types: list = [], min: int = 1, max: int = 0) -> None:
    """Check the structure of `test_table` and print any error messages.

    Use this instead of `test()` if the function to be tested is not yet implemented
    or if you want to provide specific input and output types.

    This function calls `check_table` and prints the returned error messages.

    Args:
        test_table (list|tuple): The sequence of tests, each one a list or
            tuple with: a string (the test name); zero or more values (the inputs to the function);
            the expected output value.
        types (list): Expected types of the inputs and output.
            Set this argument only if the number and order of inputs are fixed.
        min (int): Minimum number of tests in the table. Default is 1.
        max (int): Maximum number of tests in the table. Default is 0 (no maximum).
    """
    if errors := check_table(test_table, types, min, max):
        for error in errors:
            print(f"Error: {error}.")
    else:
        print("OK: the test table passed the automatic checks.")

def test(function: Callable, test_table: list | tuple, min: int = 1, max: int = 0) -> None:
    """Test `function` with `test_table`. Report errors in the table and failed tests.

    This function checks that:

    - the table is a list or tuple with at least `min` tests
    - the table has at most `max` tests (if `max` is greater than 0)
    - each test is a list or tuple with a string followed by one or more values
    - each test has the expected number of inputs (if `function` has fixed arguments).

    Args:
        function (Callable): The function or method to be tested.
        test_table (list|tuple): The sequence of tests, each one a list or
            tuple with: a string (the test name); zero or more values (the inputs to the function);
            the expected output value.
        min (int): Minimum number of tests in the table. Default is 1.
        max (int): Maximum number of tests in the table. Default is 0 (no maximum).
    """
    sig = signature(function)
    params = sig.parameters.values()
    # Determine if the function has variable number arguments (*args, **kwargs, default args)
    has_variable_args = any(
        p.default != Parameter.empty
        or p.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD)
        for p in params
    )
    # Check number of values (args + output) only if args are fixed.
    types = [] if has_variable_args else [object] * (len(params) + 1)
    if errors := check_table(test_table, types, min, max):
        for error in errors:
            print(f"Error: {error}.")
        print(f"{function.__name__} was NOT tested.")
    else:
        print(f"Testing {function.__name__}...")
        passed = failed = 0
        for test in test_table:
            name = test[0]
            inputs = test[1:-1]
            expected = test[-1]
            try:
                actual = function(*inputs)
                if actual != expected:
                    print(name, "FAILED:", actual, "instead of", expected)
                    failed += 1
                else:
                    passed += 1
            except Exception as e:
                print(name, "FAILED:", e)
                failed += 1
        percentage = round(passed / (passed + failed) * 100) if passed + failed > 0 else 0
        print(f"Tests finished: {passed} passed ({percentage}%), {failed} failed.")
