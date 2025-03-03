import pytest
import algoesup
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output

RUFF_FOUND = "**ruff** found issues:\n\n"
ALLOWED_FOUND = "**allowed** found issues:\n\n"


def ruff_warning(line_num: int, error_code: str, name: str, message: str) -> str:
    """Generate a raw markdown ruff warning"""
    return rf"- {line_num}: \[[{error_code}](https://docs.astral.sh/ruff/rules/{name})\] {message}"


def allowed_warning(line_num: int, message: str) -> str:
    """Generate a raw markdown allowed warning"""
    return f"- {line_num}: {message}"


# fmt: off
ruff_defaults_tests = [
    (
        "max = 0",
        RUFF_FOUND
        + ruff_warning(
            1,
            "A001",
            "builtin-variable-shadowing",
            "Variable `max` is shadowing a Python builtin",
        ),
    ),
    (
        "x = 42\ny = ++x",
        RUFF_FOUND
        + ruff_warning(
            2, 
            "B002",
            "unary-prefix-increment-decrement",
            "Python does not support the unary prefix increment operator (`++`)",
        ),
    ),
    (
        "def f():\n    pass",
        RUFF_FOUND
        + ruff_warning(
            1,
            "D103",
            "undocumented-public-function",
            "Missing docstring in public function",
        ),
    ),
    (
        "l = 42",
        RUFF_FOUND
        + ruff_warning(
            1,
            "E741",
            "ambiguous-variable-name",
            "Ambiguous variable name: `l`",
        ),
    ),
    (
        (
        "def function(x):\n"
        '    """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis auctor purus ut ex fermentum, at maximus est hendrerit."""\n'
        "    pass"
        ),
        RUFF_FOUND
        + ruff_warning(
            2,
            "E501",
            "line-too-long",
            "Line too long (127 > 88)",
        ),
    ),
    (
        (
            "from os import path\n\n"
            "for path in files:\n"
            "   print(path)"
        ),
        RUFF_FOUND
        + ruff_warning(
            3, 
            "F402",
            "import-shadowed-by-loop-var",
            "Import `path` from line 1 shadowed by loop variable",
        ),
    ),
    (
        (
            "def myFunction():\n"
            '    """Pass."""\n'
            "    pass"
        ),
        RUFF_FOUND
        + ruff_warning(
            1,
            "N802",
            "invalid-function-name",
            "Function name `myFunction` should be lowercase",
        ),
    ),
    (
        "import numpy as numpy",
        RUFF_FOUND
        + ruff_warning(
            1, 
            "PLC0414",
            "useless-import-alias",
            "Import alias does not rename original package. Suggested fix: Remove import alias",
        ),
    ),
]

ruff_extras_tests = [
    (
        (
            "def function(x):\n"
            '    """Pass x back to the user."""\n'
            "    return x"
        ),
        RUFF_FOUND
        + ruff_warning(
            1, 
            "ANN201",
            "missing-return-type-undocumented-public-function",
            "Missing return type annotation for public function `function`\n",
        )
        + ruff_warning(
            1, 
            "ANN001",
            "missing-type-function-argument",
            "Missing type annotation for function argument `x`",
        )
    ),
    (
        'x = "{}".format(foo)',
        RUFF_FOUND
        + ruff_warning(
                1, 
                "UP032",
                "f-string",
                "Use f-string instead of `format` call. Suggested fix: Convert to f-string",
        )
    ),
]

ruff_default_ignore_tests = [
    (
        'def func():\n """Pass."""    pass',
        RUFF_FOUND + 
        ruff_warning(
            1,
            "D100",
            "missing-docstring-in-public-module",
            "Missing docstring in public module",
        ),
    ),
    (
        'def func():\n """Pass."""    pass',
        RUFF_FOUND
        + ruff_warning(
            2,
            "W292",
            "no-newline-at-end-of-file",
            "No newline at end of file"
        )
    ),
    (
        "import os",
        RUFF_FOUND 
        + ruff_warning(
            1,
            "F401",
            "unused-import",
            "`os` imported but unused"
        )
    ),
    (
        "print(x)",
        RUFF_FOUND
        + ruff_warning(
            1, 
            "F821",
            "undefined-name",
            "Undefined name `x`"
        )
    ),
    (
        "class MyClass:\n    '''Docstring'''",
        RUFF_FOUND
        + ruff_warning(
            2,
            "D203",
            "blank-line-before-class-docstring",
            "1 blank line required before class docstring"
        )
    ),
    (
        "def func():\n    '''Summary\n    Details'''",
        RUFF_FOUND
        + ruff_warning(
            2,
            "D213",
            "multi-line-docstring-summary-not-on-second-line",
            "Multi-line docstring summary should start at the second line"
        )
    ),
    (
        "def func():\n    '''Summary without period'''",
        RUFF_FOUND
        + ruff_warning(
            2,
            "D415",
            "first-line-no-period",
            "First line should end with a period"
        )
    ),
]


allowed_tests = [
    (
        "import numpy as np", 
        ALLOWED_FOUND 
        + allowed_warning(
            1,
            "numpy"
        ),
    ),
    (
        's = f"this is a f-string"',
        ALLOWED_FOUND
        + allowed_warning(
            1,
            "f-string",
        ),
    ),
]
# fmt: on


@pytest.fixture(scope="function")
def ipython_shell():
    """Simulate the Jupyter Notebook environment and load algoesup.magics extension."""
    shell = InteractiveShell.instance()
    shell.run_cell("%load_ext algoesup.magics")
    yield shell
    # Cleanup
    shell.run_cell("%ruff off")
    shell.run_cell("%allowed off")
    shell.reset(new_session=True, aggressive=True)


def test_register_post_cell_run_event(ipython_shell: InteractiveShell) -> None:
    """Ensure run_checkers has been registered with the post_run_cell event."""
    post_run_callbacks = ipython_shell.events.callbacks.get(
        "post_run_cell",
        [],
    )
    assert "run_checkers" in [f.__name__ for f in post_run_callbacks]


def test_ruff_on_off(ipython_shell: InteractiveShell) -> None:
    """Ensure %ruff activates, deactivates and prints appropriate messages."""
    with capture_output() as captured:
        ipython_shell.run_cell("%ruff on")
    assert "ruff was activated" in captured.stdout
    assert "ruff" in algoesup.magics.active
    with capture_output() as captured:
        ipython_shell.run_cell("%ruff off")
    assert "ruff was deactivated" in captured.stdout
    assert "ruff" not in algoesup.magics.active


def test_allowed_on_off(ipython_shell: InteractiveShell) -> None:
    """Ensure %allowed activates, deactivates, and prints appropriate messages"""
    with capture_output() as captured:
        ipython_shell.run_cell("%allowed on")
    assert "allowed was activated" in captured.stdout
    assert "allowed" in algoesup.magics.active
    with capture_output() as captured:
        ipython_shell.run_cell("%allowed off")
    assert "allowed was deactivated" in captured.stdout
    assert "allowed" not in algoesup.magics.active


@pytest.mark.parametrize("test_input, expected", ruff_defaults_tests)
def test_defaults_ruff(
    ipython_shell: InteractiveShell, test_input: str, expected: str
) -> None:
    """Ensure %ruff shows warnings from a selection enabled default rules."""
    with capture_output() as captured:
        ipython_shell.run_cell("%ruff on")
        ipython_shell.run_cell(test_input)
    markdown_outputs = [
        out.data.get("text/markdown")
        for out in captured.outputs
        if hasattr(out, "data") and "text/markdown" in out.data
    ]
    assert markdown_outputs, f"No Markdown output for input: {test_input}"
    assert expected in markdown_outputs, (
        f"Expected '{expected}', got '{markdown_outputs[0]}'"
    )


@pytest.mark.parametrize("test_input, expected", ruff_defaults_tests)
def test_ignore_extras_ruff(
    ipython_shell: InteractiveShell, test_input: str, expected: str
) -> None:
    """Ensure %ruff ignores extra rules A001, B002, D103, E741, E501, F402, N802 and PLC0414."""
    with capture_output() as captured:
        ipython_shell.run_cell(
            "%ruff on --ignore A001,B002,D103,E741,E501,F402,N802,PLC0414"
        )
        ipython_shell.run_cell(test_input)
    markdown_outputs = [
        out.data.get("text/markdown")
        for out in captured.outputs
        if hasattr(out, "data") and "text/markdown" in out.data
    ]
    assert expected not in markdown_outputs, (
        f"Expected '{expected}', got '{markdown_outputs[0]}'"
    )


@pytest.mark.parametrize("test_input, expected", ruff_default_ignore_tests)
def test_ignore_defaults_ruff(
    ipython_shell: InteractiveShell, test_input: str, expected: str
) -> None:
    """Ensure %ruff ignores rules D100, W292, F401, F821, D203, D213 and D415 by default."""
    with capture_output() as captured:
        ipython_shell.run_cell("%ruff on")
        ipython_shell.run_cell(test_input)
    markdown_outputs = [
        out.data.get("text/markdown")
        for out in captured.outputs
        if hasattr(out, "data") and "text/markdown" in out.data
    ]
    assert expected not in markdown_outputs, (
        f"Expected '{expected}', got '{markdown_outputs[0]}'"
    )


@pytest.mark.parametrize("test_input, expected", ruff_extras_tests)
def test_extras_ruff(
    ipython_shell: InteractiveShell, test_input: str, expected: str
) -> None:
    """Ensure %ruff shows warnings for extra rules ANN and UP"""
    with capture_output() as captured:
        ipython_shell.run_cell("%ruff on --extend-select ANN,UP")
        ipython_shell.run_cell(test_input)
    markdown_outputs = [
        out.data.get("text/markdown")
        for out in captured.outputs
        if hasattr(out, "data") and "text/markdown" in out.data
    ]
    assert markdown_outputs, f"No Markdown output for input: {test_input}"
    assert expected in markdown_outputs, (
        f"Expected '{expected}', got '{markdown_outputs[0]}'"
    )


@pytest.mark.parametrize("test_input, expected", allowed_tests)
def test_allowed(
    ipython_shell: InteractiveShell, test_input: str, expected: str
) -> None:
    """Ensure %allowed shows warnings with default settings `%allowed on`"""
    with capture_output() as captured:
        ipython_shell.run_cell("%allowed on")
        ipython_shell.run_cell(test_input)
    markdown_outputs = [
        out.data.get("text/markdown")
        for out in captured.outputs
        if hasattr(out, "data") and "text/markdown" in out.data
    ]
    assert markdown_outputs, f"No Markdown output for input: {test_input}"
    assert expected in markdown_outputs, (
        f"Expected '{expected}', got '{markdown_outputs[0]}'"
    )
