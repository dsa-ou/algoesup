"""Functions, classes and methods to use in testing.

To simplify the creation of test tables, each function or method returns the sum 
of its arguments.
"""


def no_args() -> int:
    """Sum with no arguments."""
    return 0


def two_args(a: int, b: int) -> int:
    """Sum of two arguments."""
    return a + b


def var_args(*args: int) -> int:
    """Sum of variable arguments."""
    return sum(args)


def default_args(a: int, b: int = 0) -> int:
    """Sum of positional and default arguments."""
    return a + b


class Methods:
    """Methods for testing algoesup.test."""

    def no_args(self) -> int:
        """Sum with no arguments."""
        return 0

    def two_args(self, a: int, b: int) -> int:
        """Sum of two arguments."""
        return a + b

    def var_args(self, *args: int) -> int:
        """Sum of variable arguments."""
        return sum(args)

    def default_args(self, a: int, b: int = 0) -> int:
        """Sum of positional and default arguments."""
        return a + b
