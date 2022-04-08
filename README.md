# AFLuent

Spectrum Based Fault Localization made easy for Python

<!-- TODO: add logo here -->

![](./images/afluent_logo2.png)

- [AFLuent](#afluent)
  - [Installation](#installation)
  - [Running AFLuent](#running-afluent)

## Installation

Install the latest version of AFLuent using `pip`

```shell
pip install afluent
```

## Running AFLuent

```
Automated Fault Localization (AFLuent):
  --afl-debug, --afl    Enable AFLuent
  --tarantula           Enable fault localization using Tarantula
  --ochiai              Enable fault localization using Ochiai
  --ochiai2             Enable fault localization using Ochiai2
  --dstar               Enable fault localization using Dstar
  --dstar-pow=DSTAR_POW
                        Power to use when calculating Dstar score, default to 3
  --afl-results=RESULTS_NUM
                        Number of results to display in the score report ,
                        default to 20
  --afl-ignore=[AFL_IGNORE ...]
                        File patterns to ignore when calculating coverage for
                        AFLuent (example: tests/*).
  --report={json,csv,eval}
                        Store report after AFLuent run.
  --per-test-report     Get per test case coverage report.
  --tiebreaker={random,cyclomatic,logical,enhanced}
                        Type of tie breaking approach.
```
