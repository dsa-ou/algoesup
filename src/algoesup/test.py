"""Simplified testing for Python functions, see the [examples](coding.ipynb#testing)."""

from inspect import Parameter, signature
from typing import Callable


def test(function: Callable, test_table: list | tuple) -> None:
    """Test the function with the test_table. Report failed tests.

    Args:
        function (Callable): The function or method to be tested.
        test_table (list|tuple): The sequence of test cases, each one a list or
            tuple with: a string (the test case name); zero or more values (the inputs to the function);
            the expected output value.
    """
    not_tested = f"{function.__name__} was NOT tested."
    if not isinstance(test_table, (list, tuple)):
        print(f"Error: The test table must be a list or tuple.\n{not_tested}")
        return
    sig = signature(function)
    params = sig.parameters.values()
    # Determine if the function has variable number arguments (*args, **kwargs, default args)
    has_variable_args = any(
        p.default != Parameter.empty
        or p.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD)
        for p in params
    )
    expected_num_args = len(params)
    invalid = []
    for num, test_case in enumerate(test_table, start=1):
        if not isinstance(test_case, (list, tuple)):
            invalid.append(f"test case {num} must be a list or tuple")
        elif len(test_case) < 2:
            invalid.append(f"test case {num} must have at least two elements")
        elif not isinstance(test_case[0], str):
            invalid.append(f"test case {num} must have a string as first element")
        elif not has_variable_args and len(test_case[1:-1]) != expected_num_args:
            num_args = len(test_case[1:-1])
            invalid.append(
                f'test case "{test_case[0]}" has {num_args} input(s) instead of {expected_num_args}'
            )
    if invalid:
        for msg in invalid:
            print(f"Error: {msg}.")
        print(not_tested)
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
