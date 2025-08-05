"""Pytest-based tests for algoesup.test."""

import pytest
from typing import Callable, Any
from algoesup import test as run_test  # The name 'test' conflicts with pytest
from callables import no_args, two_args, var_args, default_args, Methods

error_messages = {
    "table_not_seq": "the table must be a list or tuple.",
    "case_not_list": "test {case_num} must be a list or tuple.",
    "case_short": "test {case_num} must have two or more elements.",
    "case_no_str": "test {case_num} must have a string as first element.",
    "args_count_str": "test '{name}' must have {expected} input(s) ({given} given).",
}


def valid_msg(func_name: str, passed: int, failed: int) -> str:
    """Generate a message for a valid test table"""
    percentage = round(passed / (passed + failed) * 100) if passed + failed > 0 else 0
    return f"Tests finished: {passed} passed ({percentage}%), {failed} failed."


def error_msg(error: str, **kwargs) -> str:
    """Generate an error message for an invalid test table"""
    return f"Error: {error_messages[error].format(**kwargs)}"


def not_tested_msg(func_name: str) -> str:
    """Generate the not tested message"""
    return f"{func_name} was NOT tested."


# Each test case:
#   (
#       ID (str): a unique, descriptive identifier for the test case,
#       Function/Method (callable): the function or method passed to algoesup.test,
#       Test Table (Any): test data for the function,
#       Expected Output Messages (list[str]): generated messages expected in the output
#   )
test_cases_for_test = [
    (
        "no_args - no inputs; list of lists; last case fails",
        no_args,
        [["Case 1", 0], ["Case 2", 1]],
        [valid_msg("no_args", 1, 1)],
    ),
    (
        "two_args - add two numbers; list of tuples; first case fails",
        two_args,
        [("Case 1", 2, 3, 4), ("Case 2", 5, 7, 12)],
        [valid_msg("two_args", 1, 1)],
    ),
    (
        "var_args - sum variable args; tuple of lists; all cases fail",
        var_args,
        (["Case 1", 1, 2, 3, 5], ["Case 2", 1, 2, 3, 4, 11]),
        [valid_msg("var_args", 0, 2)],
    ),
    (
        "default_args - one and two args; tuple of tuples; middle cases fail",
        default_args,
        (
            ("Case 1", 5, 5),
            ("Case 2", 5, 6),
            ("Case 3", 5, 10, 10),
            ("Case 4", 5, 10, 15),
        ),
        [valid_msg("default_args", 2, 2)],  # cases 2 and 4 fail
    ),
    (
        "Methods.no_args - no inputs; list of tuples; last case fails",
        Methods().no_args,
        [("Case 1", 0), ("Case 2", 1)],
        [valid_msg("no_args", 1, 1)],
    ),
    (
        "Methods.two_args - add two numbers; tuple of lists; no case fails",
        Methods().two_args,
        (["Case 1", 5, 7, 12], ["Case 2", 2, 3, 5]),
        [valid_msg("two_args", 2, 0)],
    ),
    (
        "Methods.var_args - sum variable args; tuple of tuples; all cases fail",
        Methods().var_args,
        (("Case 1", 4, 5, 6, 16), ("Case 2", 1, 2, 3, 4, 11)),
        [valid_msg("var_args", 0, 2)],
    ),
    (
        "Methods.default_args - one and two args; list of lists; some cases fail",
        Methods().default_args,
        [
            ["Case 1", 6, 6],
            ["Case 2", 6, 4, 10],
            ["Case 3", 4, 6, 11],
            ["Case 4", -1, 7],
        ],
        [valid_msg("default_args", 2, 2)],
    ),
    (
        "sum - built-in function; one case fails",
        sum,
        [["Case 1", [1, 2], 3], ["Case 2", 1, 2, 3], ["Case 3", [1], 2, 3]],
        [valid_msg("sum", 2, 1)],
    ),
    (
        "no_args - table isn't a list or tuple",
        no_args,
        None,
        [
            error_msg("table_not_seq"),
            not_tested_msg("no_args"),
        ],
    ),
    (
        "no_args - invalid test cases",
        no_args,
        [42, (), [0], (0, "Case 4"), "Case 5", ["Case 6", 1, 1]],
        [
            error_msg("case_not_list", case_num=1),
            error_msg("case_short", case_num=2),
            error_msg("case_short", case_num=3),
            error_msg("case_no_str", case_num=4),
            error_msg("case_not_list", case_num=5),
            error_msg("args_count_str", name="Case 6", given=1, expected=0),
            not_tested_msg("no_args"),
        ],
    ),
    (
        "two_args - some invalid cases (wrong argument counts)",
        two_args,
        [
            ["0 args", 0],
            ["1 arg", 1, 1],
            ["2 args", 2, 3, 5],
            ["3 args", 2, 3, 4, 9],
        ],
        [
            error_msg("args_count_str", name="0 args", given=0, expected=2),
            error_msg("args_count_str", name="1 arg", given=1, expected=2),
            error_msg("args_count_str", name="3 args", given=3, expected=2),
            not_tested_msg("two_args"),
        ],
    ),
]


@pytest.mark.parametrize(
    "id,func,test_table,expected_output",
    test_cases_for_test,
    ids=[case[0] for case in test_cases_for_test],
)
def test_algoesup_test(
    id: str, func: Callable, test_table: Any, expected_output: list[str], capsys
):
    """Test algoesup.test"""
    run_test(func, test_table)
    captured = capsys.readouterr()
    for message in expected_output:
        assert message in captured.out
