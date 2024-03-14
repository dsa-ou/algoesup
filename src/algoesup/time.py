"""Tools for measuring and plotting run-times"""

from typing import Callable

import timeit
import matplotlib.pyplot as plt


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
    start: int,
    double: int,
    text: bool = True,
    chart: bool = False,
) -> None:
    """Print or plot the run-times of `function` for different input cases.
    
    `time_cases` prints or plots the run-times of a single function using a list of 
    different input generators. Inputs are generated based on a starting size and are 
    doubled a specified number of times.

    Args:
        function (Callable): A function whose run-times will be measured.
        cases (list[Callable]): A list of 1 to 6 functions to generate inputs of different cases,
            e.g. best-, normal- and worst-case.
        start (int): The starting size for the inputs. Must be positive.
        double (int): The number of times to double the input size. Must be non-negative.
        text (bool, optional): If True, print the run-times in text format.
        chart (bool, optional): If True, plot the run-times using a chart.
    
    Raises:
        AssertionError: If input conditions are not satisfied.
    """
    assert start > 0, "the start size must be positive"
    assert double >= 0, "must double the input size at least zero times"
    assert 0 < len(cases) < 7, "there must be 1 to 6 input functions"
    assert text or chart, "at least one of text and chart must be enabled"

    sizes = [start]  # the input sizes used
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
    """Print or plot the run-times of different functions for the same inputs.

    `time_functions` prints or plots the run-times given list of functions and an input 
    generator. Inputs are generated based on a starting size and are doubled a specified 
    number of times.

    Args:
        functions (list[Callable]): A list of functions whose run-times will be measured.
            Must be 1 to 6 functions.
        inputs (Callable): A function to generate inputs when given a specific size.
        start (int): The starting size for the inputs. Must be positive.
        double (int): The number of times to double the input size. Must be non-negative.
        text (bool, optional): If True, print the run-times in text format
        chart (bool, optional): If True plot the run-times using a chart.
        value (bool, optional): If True x-axis is labelled "Input value" otherwise "Input size".

    Raises:
        AssertionError: If input conditions are not satisfied.
    """
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
    start: int = 1,
    double: int = 10,
    text: bool = True,
    chart: bool = True,
) -> None:
    """Time functions that take a single integer as input.
    
    `time_functions_int` uses `time_functions` to measure and display the run-times
    of a given list of functions that accept a single integer input. The integer inputs
    are generated starting from a specified value that defaults to 1, and are doubled
    a specified number of times that defaults to 10.

    Args:
        functions (list[Callable]): A list of functions whose run-times will be measured.
            Each function must accept a single integer argument. Must be 1 to 6 functions.
        generator (Callable, optional): A function to generate integer inputs. Defaults to
            `int_value`, which returns a tuple containing the input integer.
        start (int, optional): The starting integer value for inputs. Defaults to 1.
            Must be positive.
        double (int, optional): The number of times to double the input integer value.
            Defaults to 10. Must be non-negative.
        text (bool, optional): If True, print the run-times in text format. 
        chart (bool, optional): If True, plot the run-times using a chart. 
    """
    time_functions(functions, generator, start, double, text, chart, True)
