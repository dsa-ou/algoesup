"""Simplified testing for Python functions, see the [examples](coding.ipynb#testing)."""

from inspect import ismethod
from typing import Callable


def test(function: Callable, test_table: list) -> None:
    """Test the function with the test_table. Report failed tests.

    Args:
        function (Callable): The function to be tested. Can't be a built-in function.
        test_table (list): The list of tests. Each element of test_table is a list or
            tuple with: a string (the test case name); one or more values (the inputs to the function);
            the expected output value.
    """
    not_tested = f"The test table is invalid, {function.__name__} has NOT been tested."
    if not isinstance(test_table, (list, tuple)):
        print(f"Error: The test table must be a list or tuple.\n{not_tested}")
        return
    param_count = function.__code__.co_argcount
    # Methods don't require instance (self) argument when called.
    expected_num_args = param_count if not ismethod(function) else param_count - 1
    invalid = []
    for num, test_case in enumerate(test_table, start=1):
        if not isinstance(test_case, (list, tuple)):
            invalid.append(f"test case {num} must be a list or tuple.")
        elif not isinstance(test_case[0], str):
            invalid.append(f"test case {num} must have string as first element.")
        elif len(test_case[1:-1]) != expected_num_args:
            num_args = len(test_case[1:-1])
            invalid.append(
                f'test case "{test_case[0]}" has {num_args} input(s) instead of {expected_num_args}'
            )
    if invalid:
        for msg in invalid:
            print(f"Error: {msg}")
        print(not_tested)
        return
    else:
        print(f"Testing {function.__name__}...")
        passed = failed = 0
        for test_case in test_table:
            name = test_case[0]
            inputs = test_case[1:-1]
            expected = test_case[-1]
            actual = function(*inputs)
            if actual != expected:
                print(name, "FAILED:", actual, "instead of", expected)
                failed += 1
            else:
                passed += 1
        print("Tests finished:", passed, "passed,", failed, "failed.")
