"""Simplified testing for Python functions, see the [examples](coding.ipynb#testing)."""

from inspect import Parameter, signature
from typing import Callable

def check_table(test_table: list | tuple, types: list = [], min: int = 1, max: int = 0) -> list:
    """Check the structure of the table and return a list of error messages."""
    if min < 0 or max < 0:
        raise ValueError("Minimum and maximum number of tests can't be negative.")
    if not isinstance(test_table, (list, tuple)):
        return ["The test table must be a list or tuple"]
    messages = []
    for number, test in enumerate(test_table, start=1):
        if not isinstance(test, (list, tuple)):
            messages.append(f"test case {number} must be a list or tuple")
        elif len(test) < 2:
            messages.append(f"test case {number} must have at least two elements")
        elif not isinstance(test[0], str):
            messages.append(f"test case {number} must have a string as first element")
        elif types:
            name = test[0]
            if len(types) != len(test) - 1:
                messages.append(f'test case "{name}" has {len(test)-2} input(s) instead of {len(types)-1}')
            for value, expected_type in zip(test[1:], types):
                if not isinstance(value, expected_type):
                    messages.append(f'in test "{name}", {value} hasn\'t type {expected_type.__name__}')
    if len(test_table) < min:
        messages.append(f'the table has fewer than {min} test{"" if min == 1 else "s"}')
    elif len(test_table) > max > 0:
        messages.append(f"the table has more than {max} tests")
    return messages

def check_tests(test_table: list | tuple, types: list = [], min: int = 1, max: int = 0) -> None:
    """Check the structure of the table and print any error messages."""
    if errors := check_table(test_table, types, min, max):
        for error in errors:
            print(f"Error: {error}.")
    else:
        print("OK: the test table seems to be well defined.")

def test(function: Callable, test_table: list | tuple, min: int = 1, max: int = 0) -> None:
    """Test the function with the test_table. Report failed tests.

    Args:
        function (Callable): The function or method to be tested.
        test_table (list|tuple): The sequence of test cases, each one a list or
            tuple with: a string (the test case name); zero or more values (the inputs to the function);
            the expected output value.
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
        for test_case in test_table:
            name = test_case[0]
            inputs = test_case[1:-1]
            expected = test_case[-1]
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
        print(f"Tests finished: {passed} ({percentage}%) passed, {failed} failed.")
