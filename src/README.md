# Algoesup 

This small library was written to support the writing of 
[algorithmic essays](https://dsa-ou.github.io/algoesup),
but can be used independently of that purpose. 
The library provides auxiliary functions that make it easier to:
 - write unit tests for functions
 - measure and plot run-times for best, average and worst case inputs
 - use linters within Jupyter Notebook environments.

Guidance on how to use the library is [here](https://dsa-ou.github.io/algoesup/writing/#code).

To install in the global Python environment, open a terminal or PowerShell, and enter
```bash
pip install algoesup
```
To install in a virtual environment, activate it before entering the command above.

The library supports the [ruff](https://docs.astral.sh/ruff) and 
[allowed](https://dsa-ou.github.io/allowed) linters, and the 
[pytype](https://google.github.io/pytype) type checker.
You have to install them explicitly if you want to use them from within a notebook:
```bash
pip install ruff allowed pytype
```
Note that `pytype` is not available for Windows.

## Licence

`algoesup` is Copyright © 2023–2024 by The Open University, UK. 
The code is licensed under a 
[BSD 3-clause licence](https://github.com/dsa-ou/algoesup/blob/main/LICENSE). 
The documentation is licensed under a 
[Creative Commons Attribution 4.0 International Licence](https://creativecommons.org/licenses/by/4.0/)