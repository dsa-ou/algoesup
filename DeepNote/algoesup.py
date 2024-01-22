import json
import os
import re
import subprocess
import sys
import tempfile
import timeit
from typing import Callable

import matplotlib.pyplot as plt
from IPython.core.inputtransformer2 import TransformerManager
from IPython.core.magic import register_line_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import display_markdown

# Testing functions
# -----------------


def test(function: Callable, test_table: list) -> None:
    """Test the function with the test_table. Report failed tests.

    Preconditions: each element of test_table is a list or tuple with
        - a string (the test case name)
        - one or more values (the inputs to the function)
        - the expected output value
    """
    print(f"Testing {function.__name__}:")
    for test_case in test_table:
        name = test_case[0]
        inputs = test_case[1:-1]
        expected = test_case[-1]
        actual = function(*inputs)
        if actual != expected:
            print(name, "FAILED:", actual, "instead of", expected)
    print("Tests finished.")


# Input generators
# ----------------


def int_value(n: int) -> tuple[int]:
    """Return the value n."""
    return (n,)


# Timing functions
# -----------------


def scale_and_unit(seconds: float) -> tuple[int, str]:
    """Given a time in seconds, return the appropriate scale factor and time unit."""
    if seconds < 1e-6:
        return 1_000_000_000, "ns"
    if seconds < 1e-3:
        return 1_000_000, "µs"
    if seconds < 1:
        return 1_000, "ms"
    return 1, "s"


def time_it(function: Callable, *args, loops=0, repeat=3) -> float:
    """Return the fastest time, in seconds, of running `function` on `*args`.

    By default (zero loops), use enough loops to take >= 0.2 seconds.
    """
    assert loops >= 0, "loops must be non-negative"
    assert repeat > 0, "repeat must be positive"

    timer = timeit.Timer(lambda: function(*args))
    if loops == 0:
        loops, run_time = timer.autorange()
        run_times = timer.repeat(repeat - 1, loops)
        run_times.append(run_time)
    else:
        run_times = timer.repeat(repeat, loops)
    return min(run_times) / loops


def time_cases(
    function: Callable,
    cases: list[Callable],
    start_size: int,
    double: int,
    text: bool = True,
    chart: bool = False,
) -> None:
    """Print or plot the run-times of `function` for different input cases."""
    assert start_size > 0, "the start size must be positive"
    assert double >= 0, "must double the input size at least zero times"
    assert 0 < len(cases) < 7, "there must be 1 to 6 input functions"
    assert text or chart, "at least one of text and chart must be enabled"

    sizes = [start_size]  # the input sizes used
    for _ in range(double):
        sizes.append(sizes[-1] * 2)
    scale = unit = None  # no scale determined yet
    if chart:
        markers = ["bo-", "ko--", "ro:", "ys-", "cs--", "gs:"]
        times: list[list[float]] = []
        for _ in range(len(cases)):
            times.append([])
        plt.title(f"Run-times for {function.__name__}")
    if text:
        print(f"Run-times for {function.__name__}\n")
        print("Input size", end=" ")
        for case in cases:
            print(f"{case.__name__[:15]:>15}", end=" ")
    for size in sizes:
        if text:
            print(f"\n{size:>10}", end=" ")
        for index in range(len(cases)):
            instance = cases[index](size)
            run_time = time_it(function, *instance)
            if not scale:
                scale, unit = scale_and_unit(run_time)
            run_time = run_time * scale
            if chart:
                times[index].append(run_time)
            if text:
                print(f"{run_time:>15.1f}", end=" ")
        if text:
            print(f"{unit}", end="")
    if chart:
        plt.xlabel("Input size")
        plt.ylabel(f"Run-time ({unit})")
        for index in range(len(cases)):
            plt.plot(sizes, times[index], markers[index], label=cases[index].__name__)
        plt.legend()
        plt.show()


def time_functions(
    functions: list[Callable],
    inputs: Callable,
    start: int,
    double: int,
    text: bool = True,
    chart: bool = False,
    value: bool = False,
) -> None:
    """Print or plot the run-times of different functions for the same inputs."""
    assert start > 0, "the start size/value can't be negative"
    assert double >= 0, "must double the input size/value at least zero times"
    assert 0 < len(functions) < 7, "there must be 1 to 6 functions"
    assert text or chart, "at least one of text and chart must be enabled"

    x_label = "Input " + ("value" if value else "size")
    text_width = len(x_label)
    sizes = [start]  # the input sizes used
    for _ in range(double):
        sizes.append(sizes[-1] * 2)
    scale = unit = None  # no scale determined yet
    if chart:
        markers = ["bo-", "ko--", "ro:", "ys-", "cs--", "gs:"]
        times: list[list[float]] = []
        for _ in range(len(functions)):
            times.append([])
        plt.title(f"Inputs generated by {inputs.__name__}")
    if text:
        print(f"Inputs generated by {inputs.__name__}\n")
        print(x_label, end=" ")
        for index in range(len(functions)):
            print(f"{functions[index].__name__[:15]:>15}", end=" ")
    for size in sizes:
        if text:
            print(f"\n{size:>{text_width}}", end=" ")
        instance = inputs(size)
        for index in range(len(functions)):
            run_time = time_it(functions[index], *instance)
            if not scale:
                scale, unit = scale_and_unit(run_time)
            run_time = run_time * scale
            if chart:
                times[index].append(run_time)
            if text:
                print(f"{run_time:>15.1f}", end=" ")
        if text:
            print(f"{unit}", end="")
    if chart:
        plt.xlabel(x_label)
        plt.ylabel(f"Run-time ({unit})")
        for index in range(len(functions)):
            plt.plot(
                sizes, times[index], markers[index], label=functions[index].__name__
            )
        plt.legend()
        plt.show()


def time_functions_int(
    functions: list[Callable],
    generator: Callable = int_value,
    start_size: int = 1,
    double: int = 10,
    text: bool = True,
    chart: bool = True,
) -> None:
    """Time functions that take a single integer as input."""
    time_functions(functions, generator, start_size, double, text, chart, True)


# Linting functions
# -----------------

# Output processors
# ===
# These functions extract error messages from the checker's output and
# display them as an unnumbered Markdown list.


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
    "allowed": ("python allowed.py", show_errors),
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
    checkers["allowed"] = (f"python allowed.py {config}", show_errors)
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


get_ipython().events.register("post_run_cell", run_checkers)  # type: ignore[name-defined]
