# Changelog

This file documents notable changes to the `algoesup` library.
Changes to the resources (documentation, example essays, etc.) are not listed.
The format is based on [Keep a Changelog](https://keepachangelog.com). <!-- ,
with an additional 'Development' section for changes that don't affect users. -->
This project does *not* adhere to [Semantic Versioning](https://semver.org).

<!-- Per release: Added / Changed / Deprecated / Removed / Fixed / Security -->

## [Unreleased](https://github.com/dsa-ou/algoesup/compare/v0.4...HEAD)
These changes are in the GitHub repository but not on [PyPI](https://pypi.org/project/algoesup).

<!-- Nothing yet. -->

### Fixed
- don't show Ruff's `invalid-syntax` messages

## [0.4](https://github.com/dsa-ou/algoesup/compare/v0.3.1...v0.4) - 2025-08-11
### Added
- new function to check test table before writing function to be tested
- allow testing of methods, built-in functions, and variable/default args
- catch and report test exceptions as failed tests
- check that each test has at least two items: name and expected output
- check that each test's inputs and output have expected types (if given)
- report percentage of passed tests
- Ruff checks type annotations by default

### Changed
- Ruff reads cells via stdin rather than files
- Ruff doesn't check all pylint violations by default, only errors

### Fixed
- remove `output-format` from wrong TOML section to avoid parsing error
- make Ruff ignore long lines that were converted from IPython

## [0.3.1](https://github.com/dsa-ou/algoesup/compare/v0.3.0...v0.3.1) - 2024-08-17
### Fixed
- add blank line before generated Markdown list of issues

## [0.3.0](https://github.com/dsa-ou/algoesup/compare/v0.2.0...v0.3.0) - 2024-08-14
### Changed
- make `test(function, tests)` more robust by reporting malformed `tests`,
  e.g. haven't expected number of inputs
- pass any options after `on` to the linter, e.g. `%allowed on --unit 10`,
  instead of parsing them in algoesup
- catch and report errors when running linters, e.g. unknown options

## [0.2.0](https://github.com/dsa-ou/algoesup/compare/v0.1.0...v0.2.0) - 2024-03-16
### Added
- calls to `test()` report how many tests passed and failed

### Changed
- rename the timing functions argument `start_size` to `start` for consistency
- configure linters via CLI call on each cell, not TOML file, for flexibility

### Fixed
- character escape issue on Windows for `allowed` linter
- display of magics in library documentation

## [0.1.0](https://github.com/dsa-ou/algoesup/releases/tag/v0.1.0) - 2024-02-27

### Changed
- reorganise library to put it on PyPi
