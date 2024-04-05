"""Linting tools for Jupyter Notebook environments"""

import argparse
import json
import os
import re
import subprocess
import tempfile
from typing import Callable
from subprocess import CompletedProcess

from IPython.core.inputtransformer2 import TransformerManager
from IPython.core.magic import register_line_magic
from IPython.display import display_markdown


def show_allowed_errors(checker: str, output: CompletedProcess, filename: str) -> None:
    """Print the errors for the given file in allowed's output."""
    if output.returncode > 0:
        display_markdown(f"**{checker}** didn't check code:", raw=True)
        print(output.stderr if output.stderr else output.stdout)
    else:
        md = [f"**{checker}** found issues:"]
        for line in output.stdout.split("\n"):
            if "syntax" in line.lower() and "error" in line.lower():
                continue  # syntax errors already reported when running the cell
            if m := re.match(rf".*{filename}[^\d]*(\d+[^:]*:.*)", line):
                md.append(f"- {m.group(1)}")
        if len(md) > 1:
            display_markdown("\n".join(md), raw=True)


def show_ruff_json(checker: str, output: CompletedProcess, filename: str) -> None:
    """Print the errors in ruff's JSON output for the given file."""
    if output.stderr:
        # ignore syntax errors: they're reported on running the cell
        if "Failed to parse" in output.stderr:
            return
        text = "has warning:" if "warning" in output.stderr.lower() else "didn't check code:"
        display_markdown(f"**{checker}** {text}", raw=True)
        print(output.stderr)
    if errors := json.loads(output.stdout):
        md = [f"**{checker}** found issues:"]
        # the following assumes errors come in line order
        for error in errors:
            line = error["location"]["row"]
            code = error["code"]
            url = error["url"]
            msg = error["message"]
            if error["fix"]:
                msg += f". Suggested fix: {error['fix']['message']}"
            md.append(rf"- {line}: \[[{code}]({url})\] {msg}")
        display_markdown("\n".join(md), raw=True)


def show_pytype_errors(checker: str, output: CompletedProcess, filename: str) -> None:
    """Print the errors in pytype's output for the given file."""
    if output.stderr:
        text = "has warning:" if "warning" in output.stderr.lower() else "didn't check code:"
        display_markdown(f"**{checker}** {text}", raw=True)
        print(output.stderr)
    md = [f"**{checker}** found issues:"]
    for error in output.stdout.split("\n"):
        if "syntax" in error.lower() and "error" in error.lower():
            continue  # syntax errors already reported when running the cell
        if "python-compiler-error" in error:
            continue
        if m := re.match(rf".*{filename}[^\d]*(\d+)[^:]*:(.*)\[(.*)\]", error):
            line = m.group(1)
            msg = m.group(2)
            code = m.group(3)
            md.append(
                rf"- {line}:{msg}\[[{code}](https://google.github.io/pytype/errors.html#{code})\]"
            )
    if len(md) > 1:
        display_markdown("\n".join(md), raw=True)

# register the supported checkers, their commands and the output processor
checkers: dict[str, tuple[str, Callable]] = {
    "pytype": [["pytype"], show_pytype_errors],
    "allowed": [["allowed"], show_allowed_errors],
    "ruff": [["ruff", "check", "--output-format", "json"], show_ruff_json],
}
# initially no checker is active
active: set[str] = set()


def process_status(name: str, status: str) -> None:
    """Process the status of a checker."""
    if status is None:
        print(name, "is", "active" if name in active else "inactive")
    elif status == "on":
        active.add(name)
        print(name, "was activated")
    elif status == "off":
        active.discard(name)
        print(name, "was deactivated")


@register_line_magic
def pytype(line: str) -> None:
    """Activate/deactivate the [pytype linter](https://google.github.io/pytype).

    When active, the linter checks each code cell that is executed for type errors.

    - `%pytype on ...` activates the linter with the command options given after `on`
    - `%pytype on` is equal to `%pytype on --disable name-error,import-error`
    - `%pytype off` deactivates the linter
    - `%pytype` shows the current status of the linter
    - `%pytype?` shows this documentation and the command's options

    For a list of possible options `...`, enter `!pytype -h` in a code cell.
    Some options may not be appropriate when running pytype within a notebook.

    The `--disable` option expects a list of
    [errors](https://google.github.io/pytype/errors.html) to ignore, without spaces.
    By default, `%pylint` ignores these errors:

    - name-error: cells often use names defined in previous cells
    - import-error: pytype doesn't find local modules
    """
    parser = argparse.ArgumentParser("pytype")
    parser.add_argument("status",
        choices=["on", "off"],
        type=str.lower,
        help="Activate or deactivate the linter. If omitted, show the current status.",
        nargs="?",
        default=None,
    )
    parser.add_argument("-d", "--disable",
        default="name-error,import-error",
        help="Comma or space-separated list of error names to ignore",
    )
    known, unknown = parser.parse_known_args(line.split())
    if known.status != "on" and (known or unknown):
        print("warning: ignoring additional options for %pytype")
    else:
        checkers["pytype"][0] = ["pytype", "--disable", known.disable] + unknown
    process_status("pytype", known.status)


@register_line_magic
def allowed(line: str) -> None:
    """Activate/deactivate the [allowed linter](https://dsa-ou.github.io/allowed).

    When active, the linter checks each code cell that is executed for any
    Python constructs that are not listed in the given configuration file.

    - `%allowed on ...` activates the linter with any command options given after `on`
    - `%allowed on` is equal to `%allowed on --config m269.json`
    - `%allowed off` deactivates the linter
    - `%allowed` shows the current status of the linter
    - `%allowed?` shows this documentation and the command's options

    For a list of possible options `...`, enter `!allowed -h` in a code cell.
    Some options may not be appropriate when running `allowed` within a notebook.

    The `--config` option expects `m269.json`, `tm112.json` or the name of a JSON file
    with your own [configuration](https://dsa-ou.github.io/allowed/docs/configuration.html).
    """
    parser = argparse.ArgumentParser("allowed")
    parser.add_argument("status",
        choices=["on", "off"],
        type=str.lower,
        help="Activate or deactivate the linter. If omitted, show the current status.",
        nargs="?",
        default=None,
    )
    parser.add_argument("-c", "--config",
        default=None,
        help="Use configuration file CONFIG (default: m269.json).",
    )
    known, unknown = parser.parse_known_args(line.split())
    if known.status != "on" and (known or unknown):
        print("warning: ignoring additional options for %allowed")
    else:
        config = ["-c", known.config] if known.config else []
        checkers["allowed"][0] = ["allowed"] + config + unknown
    process_status("allowed", known.status)


@register_line_magic
def ruff(line: str) -> None:
    """Activate/deactivate the [Ruff linter](https://docs.astral.sh/ruff).

    When active, the linter checks each code cell that is executed
    against the selected code style rules.

    - `%ruff on ...` activates the linter with any command options given after `on`
      (see [ruff's list of rules])
    - `%ruff on` is equal to `%ruff on --select A,B,C90,D,E,W,F,N,PL --ignore D100,W292,F401,F821,D203,D213,D415`
    - `%ruff off` deactivates the linter
    - `%ruff` shows the current status of the linter
    - `%ruff?` shows this documentation

    The command `%ruff on ...` will run `ruff check --output-format json ...` on each cell.
    For a list of the possible options `...`, enter `!ruff help check` in a code cell.
    Some options may not be appropriate when running Ruff within a notebook.

    The `--select` and `--ignore` options expect a list
    of [rule codes](https://docs.astral.sh/ruff/rules), without spaces.

    By default, `%ruff` enables the rules from
    flake8-builtins (A), flake8-bugbear (B), mccabe (C90), pydocstyle (D),
    pycodestyle (E, W), pyflakes (F), pep8-naming (N), and pylint (PL).

    By default, `%ruff` ignores these rules:

    - D100: Missing docstring in public module (notebooks aren't modules)
    - W292: No newline at end of file (cells don't have a trailing blank line)
    - F401: Imported but unused (cells often import modules that are used later)
    - F821: Undefined name (cells often use names defined in previous cells)
    - D203: use D211 instead (no blank line before class docstring)
    - D213: use D212 instead (docstring starts right after \"\"\")
    - D415: use D400 instead (first line of docstring must end in .)
    """
    parser = argparse.ArgumentParser("ruff")
    parser.add_argument("status",
        choices=["on", "off"],
        type=str.lower,
        help="Activate or deactivate the linter. If omitted, show the current status.",
        nargs="?",
        default=None,
    )
    parser.add_argument("--select",
        help="Comma-separated list of rule codes to enable",
        type=str,
        default="A,B,C90,D,E,W,F,N,PL",
    )
    parser.add_argument("--ignore",
        help="Comma-separated list of rule codes to ignore",
        type=str,
        default="D100,W292,F401,F821,D203,D213,D415",
    )
    known, unknown = parser.parse_known_args(line.split())
    if known.status != "on" and (known or unknown):
        print("warning: ignoring additional options for %ruff")
    else:
        base = ["ruff", "check", "--output-format", "json"]
        rules = ["--select", known.select, "--ignore", known.ignore]
        checkers["ruff"][0] = base + rules + unknown
    process_status("ruff", known.status)


def run_checkers(result) -> None:
    """Run all active checkers after a cell is executed."""
    if not active:
        return
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp:
            # transform IPython to pure Python to avoid linters reporting syntax errors
            temp.write(TransformerManager().transform_cell(result.info.raw_cell))
            # Handle Windows file paths
            temp_name = temp.name.replace("\\", "/")
        for checker in active:
            command, display = checkers[checker]
            lint_file = command + [temp_name]
            try:
                output = subprocess.run(
                    lint_file, capture_output=True, text=True, check=False,
                )
                display(checker, output, temp_name)
            except Exception as e:
                print(f"Error on executing {command[0]}:\n{e}")
    except Exception as e:
        print(f"Error on writing cell to a temporary file:\n{e}")
    finally:
        os.remove(temp_name)


def load_ipython_extension(ipython):
    """Load the ipython extension, and register run_checkers with post_cell_run

    This function hooks into the ipython extension system so the magic commands defined
    in this module can be loaded with `load_ext algoesup.magics`. It also registers
    `run_checkers` with the `post_run_cell` event so the linters are run with the
    contents of each ipython cell after it has been executed.
    """
    ipython.events.register("post_run_cell", run_checkers)  # type: ignore[name-defined]
