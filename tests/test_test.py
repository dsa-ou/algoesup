"""Pytest-based tests for algoesup.test."""

import pytest
from typing import Callable, Any
from algoesup import test as run_test  # The name 'test' conflicts with pytest
from callables import no_args, two_args, var_args, default_args, Methods

error_messages = {
    "not_list": "The test table must be a list or tuple.",
    "case_not_list": "test case {case_num} must be a list or tuple.",
    "case_name_num": "test case {case_num} must have string as first element.",
    "case_name_str": 'test case "{name}" must have string as first element.',
    "args_count_num": "test case {case_num} has {given} input(s) instead of {expected}.",
    "args_count_str": 'test case "{name}" has {given} input(s) instead of {expected}.',
    "built_in": "Cannot test built-in functions.",
}


def valid_msg(func_name: str, passed: int, failed: int) -> str:
    """Generate a message for a valid test table"""
    return f"Testing {func_name}...\nTests finished: {passed} passed, {failed} failed."


def error_msg(error: str, **kwargs) -> str:
    """Generate an error message for an invalid test table"""
    return f"Error: {error_messages[error].format(**kwargs)}"


def not_tested_msg(func_name: str) -> str:
    """Generate the not tested message"""
    return f"{func_name} has NOT been tested."


# Each test case:
#   (
#       ID (str): a unique, descriptive identifier for the test case,
#       Function/Method (callable): the function or method passed to algoesup.test,
#       Test Table (Any): test data for the function,
#       Expected Output Messages (list[str]): generated messages expected in the output
#   )
test_cases_for_test = [
    (
        "no_args - valid table, no args",
        no_args,
        [["Case 1", 0]],
        [valid_msg("no_args", 1, 0)],
    ),
    (
        "two_args - valid table, add two numbers",
        two_args,
        [["Case 1", 2, 3, 5]],
        [valid_msg("two_args", 1, 0)],
    ),
    (
        "var_args - valid table, sum variable args",
        var_args,
        [["Case 1", 1, 2, 3, 6]],
        [valid_msg("var_args", 1, 0)],
    ),
    (
        "default_args - valid table, one and two args",
        default_args,
        [
            ["Case 1", 5, 5],
            ["Case 2", 5, 10, 15],
        ],
        [valid_msg("default_args", 2, 0)],
    ),
    (
        "Methods.no_args - valid table, no args method",
        Methods().no_args,
        [["Case 1", 0]],
        [valid_msg("no_args", 1, 0)],
    ),
    (
        "Methods.two_args - valid table, add two numbers method",
        Methods().two_args,
        [["Case 1", 5, 7, 12]],
        [valid_msg("two_args", 1, 0)],
    ),
    (
        "Methods.var_args - valid table, sum variable args method",
        Methods().var_args,
        [["Case 1", 4, 5, 6, 15]],
        [valid_msg("var_args", 1, 0)],
    ),
    (
        "Methods.default_args - valid table, one and two args method",
        Methods().default_args,
        [
            ["Case 1", 6, 6],
            ["Case 2", 6, 4, 10],
        ],
        [valid_msg("default_args", 2, 0)],
    ),
    (
        "no_args - invalid table, test table is None",
        no_args,
        None,
        [
            error_msg("not_list"),
            not_tested_msg("no_args"),
        ],
    ),
    (
        "no_args - invalid table, test case is an integer",
        no_args,
        [42],
        [
            error_msg("case_not_list", case_num=1),
            not_tested_msg("no_args"),
        ],
    ),
    (
        "no_args - invalid table, too many inputs in test case",
        no_args,
        [["Case 1", 1, 1]],
        [
            error_msg("args_count_str", name="Case 1", given=1, expected=0),
            not_tested_msg("no_args"),
        ],
    ),
    (
        "sum - invalid function, testing a built-in",
        sum,
        [["Case 1", [1, 2], 3]],
        [
            error_msg("built_in"),
            not_tested_msg("sum"),
        ],
    ),
    (
        "two_args - invalid table, multiple cases with wrong argument counts",
        two_args,
        [
            ["Case 1", 1, 1],
            ["Case 2", 2, 3, 4, 9],
            ["Case 3"],
        ],
        [
            error_msg("args_count_str", name="Case 1", given=1, expected=2),
            error_msg("args_count_str", name="Case 2", given=3, expected=2),
            error_msg("args_count_str", name="Case 3", given=0, expected=2),
            not_tested_msg("two_args"),
        ],
    ),
]


@pytest.mark.parametrize(
    "id,func,test_table,expected_output",
    test_cases_for_test,
    ids=[case[0] for case in test_cases_for_test],
)
def test_all_cases(
    id: str, func: Callable, test_table: Any, expected_output: list[str], capsys
):
    """Test algoesup.test"""
    run_test(func, test_table)
    captured = capsys.readouterr()
    for message in expected_output:
        assert message in captured.out
