"""Simplified testing for Python functions"""

from typing import Callable


def validate_test_table(function: Callable, test_table: list) -> list:
    """Validate the structure of a test table"""
    errors = []
    if not isinstance(test_table, (list, tuple)):
        errors.append("The test table must be a list or tuple.")
        return errors
    # The number of arguments function expects.
    expects = function.__code__.co_argcount
    for num, test_case in enumerate(test_table, start=1):
        if not isinstance(test_case, (list, tuple)):
            errors.append(f"Test case {num}: should be a list or tuple.")
        elif not isinstance(test_case[0], str):
            errors.append(f"Test case {num}: first element must be a string.")
        elif len(test_case[1:-1]) != expects:
            num_args = len(test_case[1:-1])
            errors.append(f"Test case {num}: {num_args} inputs found instead of {expects}")
    return errors
    
def test(function: Callable, test_table: list) -> None:
    """Test the function with the test_table. Report failed tests.

    Args:
        function (Callable): The function to be tested.
        test_table (list): The list of tests. Each element of test_table is a list or 
            tuple with: a string (the test case name); one or more values (the inputs to the function);
            the expected output value.
    """
    if errors := validate_test_table(function, test_table):
        print("ERROR: invalid test table:")
        for error in errors:
            print(error)
        print(f"{function.__name__} has NOT been tested.")
        return

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
