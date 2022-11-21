# AFLuent

![License](https://img.shields.io/badge/license-MIT-blue?style=flat)
![BuiltWith](https://img.shields.io/badge/Built%20With-Python-blue?style=flat&logo=python&logoColor=yellow)
![Actions Status](https://github.com/noorbuchi/AFLuent/workflows/Lint%20and%20Test/badge.svg)
![stars](https://img.shields.io/github/stars/noorbuchi/AFLuent.svg)

![](./images/afluent_logo2.png)

- [AFLuent](#afluent): A flaky-conscious fault localization Pytest Plugin
  - [Overview](#overview)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Command Line Interface](#command-line-interface)
  - [Warning Messages](#warning-messages)

## Overview

AFLuent is an automated fault localization tool built as a Pytest plugin.
It's triggered when one or more test case fails causing it to generate a ranking
of suspicious statements where the cause of the fault could possibly be.
Statements are ranked in a descending order based on a score calculated
through information from code coverage and using one of four supported
equations (Tarantula, Ochiai, Ochiai2, and DStar).

## Installation

Install the latest version of AFLuent using `pip`

```shell
pip install afluent
```

## Usage

Once AFLuent is installed, Pytest automatically detects it and begins to accept
its command line arguments. However, it must be enabled from the CLI in order
to run it.

**IMPORTANT NOTE:** AFLuent relies on coverage information collected by using
[`Coverage.py`](https://coverage.readthedocs.io/en/6.3.2/). In the case that
other Pytest that depend on `Coverage.py` are installed or active for the
session, AFLuent won't be able to collect accurate information and will cause
incorrect results. The reverse is also true, AFLuent will cause plugins like
`pytest-cov` to display incorrect coverage information. To avoid this, make sure
to use the `-p` and `-p no:<plugin_name>` flags to disable plugins when needed.
Example: use this command to run Pytest without AFLuent:

```shell
pytest -p no:afluent
```

### Command Line Interface

AFLuent arguments should be added to the Pytest command after the plugin has
been installed. Supported arguments can be viewed using the `pytest --help`
command.

- `--afl-debug` or `--afl`: these flags will enable AFLuent. None of the other
  arguments will work unless one of these flags are added.
- `--afl-ignore` one or many paths or files to ignore when running AFLuent.
  Example: `--afl-ignore tests/*` is recommended and it will stop AFLuent from
  calculating suspiciousness scores for test code.
- `--afl-results`: number of results to display after AFLuent generates a
  report. Defaults to 20 entries.
- `--tarantula`: calculate suspiciousness scores using the Tarantula equation
- `--ochiai`: calculate suspiciousness scores using the Ochiai equation
- `--ochiai2`: calculate suspiciousness scores using the Ochiai2 equation
- `--dstar`: calculate suspiciousness scores using the DStar equation
- `--op2`: calculate suspiciousness scores using the Op2 equation
- `--dstar-pow`: value of `*` to use the the DStar equation, defaults to 3
- `--tiebreaker`: Approach to use when resolving ties between statements.
  Options: `random`, `cyclomatic`, `logical`, or `enhanced`. Defaults to `random`.
- `--report`: type of report to produce following AFLuent's run. Options: `json`
  or `csv`
- `--per-test-report`: enables producing a per-test json report for failed and
  successful runs of the test suite.

Multiple equations can be used at the same time, however, the results will be
sorted based on the first one that was passed.

**Example:**

This command will run the test suite and AFLuent using both the DStar and Ochiai
equations. It will also handle ties using the logical tie breaker and ignore all
the files in the `tests` directory.

```
pytest --afl --afl-ignore tests/* --dstar --ochiai --tiebreaker logical
```

## Warning Messages

There are few warning messages that AFLuent produces in some instances, none of
which will prevent the tool from running but they could indicate that there is
an issue that should be checked.

- `AFLuent is disabled`: This message will show up when AFLuent is installed but
  not enabled using one of the enable flags, if you're not planning to use
  AFLuent, this message can be ignored.
- `pytest_cov plugin conflicts with AFLuent` this warning is shown when
  `pytest-cov` is detected in the same session as AFLuent. In order to fix this,
  make sure to run AFLuent with the `-p no:pytest_cov` argument to disable
  `pytest-cov`
- `Exit after failure detected`: AFLuent will display this error message when
  the exit after failure arguments are detected. Pytest options such as `-x` and
  `--maxfail` exit the session on the first failure which could prevent AFLuent
  from collecting the information needed to show an accurate ranking. For the
  best results, make sure that the full test suite runs.
