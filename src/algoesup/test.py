"""Simplified testing for Python functions"""

from typing import Callable


def test(function: Callable, test_table: list) -> None:
    """Test the function with the test_table. Report failed tests.

    Args:
        function (Callable): The function to be tested.
        test_table (list): The list of tests. Each element of test_table is a list or 
            tuple with: a string (the test case name); one or more values (the inputs to the function);
            the expected output value.
    """
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
