""" Integrate code checking tools into Jupyter Notebook environments

Usage:
    To enable magics, use `%load_ext algoesup.magics` in a cell
"""

import json
import os
import re
import subprocess
import tempfile
from typing import Callable

from IPython.core.inputtransformer2 import TransformerManager
from IPython.core.magic import register_line_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import display_markdown


def show_errors(checker: str, output: str, filename: str) -> None:
    """Print the errors for the given file in the checker's output."""
    md = [f"**{checker}** found issues:"]
    for line in output.split("\n"):
        if "syntax" in line.lower() and "error" in line.lower():
            continue  # syntax errors already reported when running the cell
        if m := re.match(rf".*{filename}[^\d]*(\d+[^:]*:.*)", line):
            md.append(f"- {m.group(1)}")
    if len(md) > 1:
        display_markdown("\n".join(md), raw=True)


def show_ruff_json(checker: str, output: str, filename: str) -> None:
    """Print the errors in ruff's JSON output for the given file."""
    if errors := json.loads(output):
        md = [f"**{checker}** found issues:"]
        # the following assumes errors come in line order
        for error in errors:
            line = error["location"]["row"]
            code = error["code"]
            url = error["url"]
            msg = error["message"]
            if error["fix"]:
                msg += f". Suggested fix: {error['fix']['message']}"
            md.append(f"- {line}: \[[{code}]({url})\] {msg}")
        display_markdown("\n".join(md), raw=True)


def show_pytype_errors(checker: str, output: str, filename: str) -> None:
    """Print the errors in pytype's output for the given file."""
    md = [f"**{checker}** found issues:"]
    for error in output.split("\n"):
        if "syntax" in error.lower() and "error" in error.lower():
            continue  # syntax errors already reported when running the cell
        if m := re.match(rf".*{filename}[^\d]*(\d+)[^:]*:(.*)\[(.*)\]", error):
            line = m.group(1)
            msg = m.group(2)
            code = m.group(3)
            md.append(
                f"- {line}:{msg}\[[{code}](https://google.github.io/pytype/errors.html#{code})\]"
            )
    if len(md) > 1:
        display_markdown("\n".join(md), raw=True)


# register the supported checkers, their commands and the output processor
checkers: dict[str, tuple[str, Callable]] = {
    "pytype": ("pytype", show_pytype_errors),
    "allowed": ("allowed", show_errors),
    "ruff": ("ruff check --output-format json", show_ruff_json),
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


@magic_arguments()
@argument(
    "status",
    choices=["on", "off"],
    type=str.lower,
    help="Activate or deactivate the linter. If omitted, show the current status.",
    nargs="?",
    default=None,
)
@register_line_magic
def pytype(line: str) -> None:
    """Activate/deactivate the `pytype` linter."""
    args = parse_argstring(pytype, line)
    process_status("pytype", args.status)


@magic_arguments()
@argument(
    "-c",
    "--config",
    default=None,
    help="Use configuration file CONFIG (default: m269.json).",
)
@argument(
    "status",
    choices=["on", "off"],
    type=str.lower,
    help="Activate or deactivate the linter. If omitted, show the current status.",
    nargs="?",
    default=None,
)
@register_line_magic
def allowed(line: str) -> None:
    """Configure and (de)activate the `allowed` linter."""
    args = parse_argstring(allowed, line)
    config = f"-c {args.config}" if args.config else ""
    checkers["allowed"] = (f"allowed {config}", show_errors)
    process_status("allowed", args.status)


@magic_arguments()
@argument(
    "status",
    choices=["on", "off"],
    type=str.lower,
    help="Activate or deactivate the linter. If omitted, show the current status.",
    nargs="?",
    default=None,
)
@register_line_magic
def ruff(line: str) -> None:
    """Activate/deactivate the `ruff` linter."""
    args = parse_argstring(ruff, line)
    process_status("ruff", args.status)


# TODO: add an option to set the output processor function
@register_line_magic
def checker(line: str) -> None:
    """Define or turn on/off a given checker."""
    global checkers, active

    args = line.split()
    if len(args) == 0:
        print("Active checkers:", *active)
        print("Inactive checkers:", *(set(checkers) - active))
        return

    name = args[0]
    if len(args) == 1:
        if name not in checkers:
            print(f"Checker {name} isn't defined.")
        else:
            status = "active" if name in active else "inactive"
            print(f"Checker {name} is {status} and defined as '{checkers[name]}'.")
    elif args[1].lower() == "on":
        if name not in checkers:
            print(f"Error: checker {name} isn't defined.")
        else:
            active.add(name)
            print(f"Checker {name} has been activated.")
    elif args[1].lower() == "off":
        if name not in checkers:
            print(f"Error: checker {name} isn't defined.")
        else:
            active.discard(name)
            print(f"Checker {name} has been deactivated.")
    else:
        command = " ".join(args[1:])
        status = "redefined" if name in checkers else "defined"
        checkers[name] = command
        active.add(name)
        print(f"Checker {name} has been {status} and activated.")


def run_checkers(result) -> None:
    """Run all active checkers after a cell is executed."""
    if not active:
        return
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp:
            # transform IPython to pure Python to avoid linters reporting syntax errors
            temp.write(TransformerManager().transform_cell(result.info.raw_cell))
            temp_name = temp.name
        for checker in active:
            command, display = checkers[checker]
            command += " " + temp_name
            try:
                output = subprocess.run(
                    command, capture_output=True, text=True, check=False, shell=True
                ).stdout
                display(checker, output, temp_name)
            except Exception as e:
                print(f"Error on executing {command}:\n{e}")
    except Exception as e:
        print(f"Error on writing cell to a temporary file:\n{e}")
    finally:
        os.remove(temp_name)


def load_ipython_extension(ipython):
    ipython.events.register("post_run_cell", run_checkers)  # type: ignore[name-defined]
