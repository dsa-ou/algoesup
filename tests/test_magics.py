"""Automated testing for %ruff and %allowed"""

import algoesup
import pytest
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output

RUFF_FOUND = "**ruff** found issues:\n\n"
ALLOWED_FOUND = "**allowed** found issues:\n\n"

# fmt: off
RUFF_WARNINGS = {
    "A001": (
        "builtin-variable-shadowing",
        "Variable `{var}` is shadowing a Python builtin"
    ),
    "B002": (
        "unary-prefix-increment-decrement",
        "Python does not support the unary prefix increment operator (`++`)"
    ),
    "D103": (
        "undocumented-public-function",
        "Missing docstring in public function"
    ),
    "E741": (
        "ambiguous-variable-name",
        "Ambiguous variable name: `{var}`"
    ),
    "E501": (
        "line-too-long",
        "Line too long ({length} > 88)"
    ),
    "F402": (
        "import-shadowed-by-loop-var",
        "Import `{var}` from line {import_line} shadowed by loop variable"
    ),
    "N802": (
        "invalid-function-name",
        "Function name `{name}` should be lowercase"
    ),
    "PLC0414": (
        "useless-import-alias",
        "Import alias does not rename original package. Suggested fix: Remove import alias"
    ),
    "ANN201": (
        "missing-return-type-undocumented-public-function",
        "Missing return type annotation for public function `{name}`. Suggested fix: Add return type annotation: `{type}`"
    ),
    "ANN001": (
        "missing-type-function-argument",
        "Missing type annotation for function argument `{arg}`"
    ),
    "UP032": (
        "f-string",
        "Use f-string instead of `format` call. Suggested fix: Convert to f-string"
    ),
    "D100": (
        "missing-docstring-in-public-module",
        "Missing docstring in public module"
    ),
    "W292": (
        "no-newline-at-end-of-file",
        "No newline at end of file"
    ),
    "F401": (
        "unused-import",
        "`os` imported but unused"
    ),
    "F821": (
        "undefined-name",
        "Undefined name `x`"
    ),
    "D203": (
        "blank-line-before-class-docstring",
        "1 blank line required before class docstring"
    ),
    "D213": (
        "multi-line-docstring-summary-not-on-second-line",
        "Multi-line docstring summary should start at the second line"
    ),
    "D415": (
        "first-line-no-period",
        "First line should end with a period"
    ),
}
# fmt: on


def ruff_warning(line_num: int, warning_code: str, **kwargs) -> str:
    """Generate a raw markdown %ruff warning"""
    error_name, message = RUFF_WARNINGS[warning_code]
    return (
        rf"- {line_num}: \[[{warning_code}](https://docs.astral.sh/ruff/rules/{error_name})\] "
        + message.format(**kwargs)
    )


def allowed_issue(line_num: int, message: str) -> str:
    """Generate a raw markdown %allowed issue"""
    return f"- {line_num}: {message}"


def get_markdown(captured: capture_output) -> list:
    """Return a list of markdown from the captured output, otherwise a list containing the empty string."""
    return [
        out.data.get("text/markdown")
        for out in captured.outputs
        if hasattr(out, "data") and "text/markdown" in out.data
    ] or [""]


# Custom assertion functions improve readability when a failure occurs
# comparing long, multiple-line strings such as raw markdown.
def assert_str_equal(actual: str, expected: str) -> None:
    """Assert two strings are equal. If not, raise a pytest fail exception."""
    if actual != expected:
        pytest.fail(
            "EXPECTED and ACTUAL did not match.\n\n"
            "=== EXPECTED ===\n"
            f"{expected}\n\n"
            "=== ACTUAL ===\n"
            f"{actual}\n",
        )


def assert_not_in_str(actual: str, unexpected: str) -> None:
    """Assert unexpected str is not in actual str. Otherwise raise a pytest fail exception."""
    if unexpected in actual:
        pytest.fail(
            "UNEXPECTED was present in ACTUAL.\n\n"
            "=== UNEXPECTED ===\n"
            f"{unexpected}\n\n"
            "=== ACTUAL ===\n"
            f"{actual}\n"
        )


# fmt: off
ruff_defaults_tests = [
    pytest.param(
        "max = 0",
        RUFF_FOUND + ruff_warning(1, "A001", var="max"),
        id="index: 0, ruff: A001",
    ),
    pytest.param(
        "x = 42\ny = ++x",
        RUFF_FOUND + ruff_warning(2, "B002"),
        id="index: 1, ruff: B002",
    ),
    pytest.param(
        "def f():\n    pass",
        RUFF_FOUND
        + ruff_warning(1, "ANN201", name="f", type="None")
        + "\n"
        + ruff_warning(1, "D103"),
        id="index: 2, ruff: ANN201+D103",
    ),
    pytest.param(
        "l = 42",
        RUFF_FOUND + ruff_warning(1, "E741", var="l"),
        id="index: 3, ruff: E741",
    ),
    pytest.param(
        'def function(x):\n    """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis auctor purus ut ex fermentum, at maximus est hendrerit."""\n    pass',
        RUFF_FOUND
        + ruff_warning(1, "ANN201", name="function", type="None")
        + "\n"
        + ruff_warning(1, "ANN001", arg="x")
        + "\n"
        + ruff_warning(2, "E501", length=127),
        id="index: 4, ruff: ANN201+ANN001+E501",
    ),
    pytest.param(
        "from os import path\n\nfor path in files:\n   print(path)",
        RUFF_FOUND + ruff_warning(3, "F402", var="path", import_line=1),
        id="index: 5, ruff: F402",
    ),
    pytest.param(
        'def myFunction():\n    """Pass."""\n    pass',
        RUFF_FOUND
        + ruff_warning(1, "N802", name="myFunction")
        + "\n"
        + ruff_warning(1, "ANN201", name="myFunction", type="None"),
        id="index: 6, ruff: N802+ANN201",
    ),
]

ruff_extras_tests = [
    pytest.param(
        'x = "{}".format(foo)',
        RUFF_FOUND + ruff_warning(1, "UP032"),
        id="index: 0, ruff: UP032",
    ),
]

ruff_default_ignore_tests = [
    pytest.param(
        'def func():\n """Pass."""    pass',
        RUFF_FOUND + ruff_warning(1, "D100"),
        id="index: 0, ruff: D100",
    ),
    pytest.param(
        'def func():\n """Pass."""    pass',
        RUFF_FOUND + ruff_warning(2, "W292"),
        id="index: 1, ruff: W292",
    ),
    pytest.param(
        "import os",
        RUFF_FOUND + ruff_warning(1, "F401"),
        id="index: 2, ruff: F401",
    ),
    pytest.param(
        "print(x)",
        RUFF_FOUND + ruff_warning(1, "F821"),
        id="index: 3, ruff: F821",
    ),
    pytest.param(
        "class MyClass:\n    '''Docstring'''",
        RUFF_FOUND + ruff_warning(2, "D203"),
        id="index: 4, ruff: D203",
    ),
    pytest.param(
        "def func():\n    '''Summary\n    Details'''",
        RUFF_FOUND + ruff_warning(2, "D213"),
        id="index: 5, ruff: D213",
    ),
    pytest.param(
        "def func():\n    '''Summary without period'''",
        RUFF_FOUND + ruff_warning(2, "D415"),
        id="index: 6, ruff: D415",
    ),
]

ruff_magics_ignore_tests = [
    pytest.param(
        "%timeit -n 1000000 -r 3 10000 + 10000 + 10000 + 10000 + 10000",
        RUFF_FOUND + ruff_warning(1, "E501", length=95),
        id="index: 0, ruff: E501",
    ),
    pytest.param(
        "for times in range(100):\n    %timeit -n 100 -r3 10000 + 10000 + 10000 + 10000 + 10000",
        RUFF_FOUND + ruff_warning(1, "E501", length=95),
        id="index: 1, ruff: E501",
    ),
    pytest.param(
        "%%capture\nfor times in range(100):\n    print('This is a long message which is part of a cell that will be captured')",
        RUFF_FOUND + ruff_warning(1, "E501", length=95),
        id="index: 2, ruff: E501",
    ),
]

ruff_mixed_tests = [
    pytest.param(
        (
            "max = 0\n"
            "x = 42\n"
            "y = ++x\n"
            "def f():\n"
            "    pass\n"
            "%timeit -n 1000000 -r 3 10000 + 10000 + 10000 + 10000 + 10000\n"
            "l = 42"
        ),
        RUFF_FOUND
        + ruff_warning(1, "A001", var="max")
        + "\n"
        + ruff_warning(3, "B002")
        + "\n"
        + ruff_warning(4, "ANN201", name="f", type="None")
        + "\n"
        + ruff_warning(4, "D103")
        + "\n"
        + ruff_warning(7, "E741", var="l"),
        id="index: 0, ruff: A001+B002+ANN201+D103+E741",
    ),
    pytest.param(
        (
            "import numpy as numpy\n"
            "from os import path\n"
            "def function(x):\n"
            '    """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis auctor purus ut ex fermentum, at maximus est hendrerit."""\n'
            "    pass\n"
            "for path in files:\n"
            "    print(path)\n"
            "def myFunction():\n"
            '    """Pass."""\n'
            "    pass"
        ),
        RUFF_FOUND
        + ruff_warning(3, "ANN201", name="function", type="None")
        + "\n"
        + ruff_warning(3, "ANN001", arg="x")
        + "\n"
        + ruff_warning(4, "E501", length=127)
        + "\n"
        + ruff_warning(6, "F402", var="path", import_line=2)
        + "\n"
        + ruff_warning(8, "N802", name="myFunction")
        + "\n"
        + ruff_warning(8, "ANN201", name="myFunction", type="None"),
        id="index: 1, ruff: ANN201+ANN001+E501+F402+N802+ANN201",
    ),
]

allowed_tests = [
    pytest.param(
        "import numpy as np",
        ALLOWED_FOUND + allowed_issue(1, "numpy"),
        id="index: 0, allowed: import numpy",
    ),
    pytest.param(
        's = f"this is an f-string"',
        ALLOWED_FOUND + allowed_issue(1, "f-string"),
        id="index: 1, allowed: f-string",
    ),
    pytest.param(
        (
            "def f(x: str):\n"
            "    if x != None:\n"
            "        x.split()"
        ),
        ALLOWED_FOUND + allowed_issue(3, "str.split()"),
        id="index: 2, allowed: str.split()",
    ),
]
# fmt: on


@pytest.fixture(scope="function")
def ipython_shell():
    """Simulate the Jupyter Notebook environment and load algoesup.magics extension."""
    shell = InteractiveShell.instance()
    shell.run_cell("%load_ext algoesup.magics")
    yield shell
    # Cleanup algoesup.magic's global state, and reset shell session.
    shell.run_cell("%ruff off")
    shell.run_cell("%allowed off")
    shell.reset(new_session=True)


def test_register_post_cell_run_event(ipython_shell: InteractiveShell) -> None:
    """Test that run_checkers has been registered with the post_run_cell event."""
    post_run_callbacks = ipython_shell.events.callbacks.get(
        "post_run_cell",
        [],
    )
    assert "run_checkers" in [f.__name__ for f in post_run_callbacks]


def test_ruff_on_off(ipython_shell: InteractiveShell) -> None:
    """Test that %ruff activates, deactivates and prints appropriate messages."""
    with capture_output() as captured:
        ipython_shell.run_cell("%ruff on")
    assert "ruff was activated" in captured.stdout
    assert "ruff" in algoesup.magics.active
    with capture_output() as captured:
        ipython_shell.run_cell("%ruff off")
    assert "ruff was deactivated" in captured.stdout
    assert "ruff" not in algoesup.magics.active


def test_allowed_on_off(ipython_shell: InteractiveShell) -> None:
    """Test that %allowed activates, deactivates, and prints appropriate messages and warnings."""
    with capture_output() as captured:
        ipython_shell.run_cell("%allowed on")
    assert "allowed was activated" in captured.stdout
    assert "allowed" in algoesup.magics.active
    with capture_output() as captured:
        ipython_shell.run_cell("%allowed off -f")
    assert (
        "warning: allowed not turned on: command options were ignored"
        in captured.stdout
    )
    assert "allowed was deactivated" in captured.stdout
    assert "allowed" not in algoesup.magics.active


@pytest.mark.parametrize("test_input, expected", ruff_defaults_tests)
def test_defaults_ruff(
    ipython_shell: InteractiveShell, test_input: str, expected: str
) -> None:
    """Test that %ruff shows warnings from a selection of enabled default rules."""
    with capture_output() as captured:
        ipython_shell.run_cell("%ruff on")
        ipython_shell.run_cell(test_input)
    markdown_outputs = get_markdown(captured)
    assert_str_equal(markdown_outputs[0], expected)


@pytest.mark.parametrize("test_input, unexpected", ruff_defaults_tests)
def test_ignore_extras_ruff(
    ipython_shell: InteractiveShell, test_input: str, unexpected: str
) -> None:
    """Test that %ruff ignores extra rules A001, B002, D103, E741, E501, F402, N802 and PLC0414."""
    with capture_output() as captured:
        ipython_shell.run_cell(
            "%ruff on --ignore A001,B002,D103,E741,E501,F402,N802,PLC0414"
        )
        ipython_shell.run_cell(test_input)
    markdown_outputs = get_markdown(captured)
    assert_not_in_str(markdown_outputs[0], unexpected)


@pytest.mark.parametrize("test_input, unexpected", ruff_default_ignore_tests)
def test_ignore_defaults_ruff(
    ipython_shell: InteractiveShell, test_input: str, unexpected: str
) -> None:
    """Test that %ruff ignores rules D100, W292, F401, F821, D203, D213 and D415 by default."""
    with capture_output() as captured:
        ipython_shell.run_cell("%ruff on")
        ipython_shell.run_cell(test_input)
    markdown_outputs = get_markdown(captured)
    assert_not_in_str(markdown_outputs[0], unexpected)


@pytest.mark.parametrize("test_input, expected", ruff_extras_tests)
def test_extras_ruff(
    ipython_shell: InteractiveShell, test_input: str, expected: str
) -> None:
    """Test that %ruff shows warnings for extra rules UP"""
    with capture_output() as captured:
        ipython_shell.run_cell("%ruff on --extend-select UP")
        ipython_shell.run_cell(test_input)
    markdown_outputs = get_markdown(captured)
    assert_str_equal(markdown_outputs[0], expected)


@pytest.mark.parametrize("test_input, unexpected", ruff_magics_ignore_tests)
def test_magics_ruff(
    ipython_shell: InteractiveShell, test_input: str, unexpected: str
) -> None:
    """Test that transformed magics don't trigger E501"""
    with capture_output() as captured:
        ipython_shell.run_cell("%ruff on")
        ipython_shell.run_cell(test_input)
    markdown_outputs = get_markdown(captured)
    assert_not_in_str(markdown_outputs[0], unexpected)


@pytest.mark.parametrize("test_input, expected", ruff_mixed_tests)
def test_mixed_ruff(
    ipython_shell: InteractiveShell, test_input: str, expected: str
) -> None:
    """Test %ruff with code that triggers multiple mixed warnings."""
    with capture_output() as captured:
        ipython_shell.run_cell("%ruff on")
        ipython_shell.run_cell(test_input)
    markdown_outputs = get_markdown(captured)
    assert_str_equal(markdown_outputs[0], expected)


@pytest.mark.parametrize("test_input, expected", allowed_tests)
def test_allowed(
    ipython_shell: InteractiveShell, test_input: str, expected: str
) -> None:
    """Test that %allowed shows warnings with default settings `%allowed on`"""
    with capture_output() as captured:
        ipython_shell.run_cell("%allowed on -m")
        ipython_shell.run_cell(test_input)
    markdown_outputs = get_markdown(captured)
    if markdown_outputs:
        assert_str_equal(markdown_outputs[0], expected)
