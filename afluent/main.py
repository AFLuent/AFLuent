"""Define Pytest Hooks that run AFLuent."""

import json
import os

import coverage  # type: ignore[import]
import pytest  # type: ignore[import]
from console import bg, fg, fx  # type: ignore[import]

from afluent import spectrum_parser


# Pytest args:
# --afluent-debug: enable, disable the plugin
# --afl-method one or many method names for afl
# --result-num number of results to display
# --afluent-ignore: ignore directories when calculating scores defaults to
# `tests`
# --afluent-config: path to the config file
# TODO: figure out what else


@pytest.hookimpl()
def pytest_sessionstart(session):
    """Create a session variable as empty dictionary to store coverage."""
    session.session_spectrum = {}


@pytest.hookimpl(hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem):
    """Calculate the coverage of each test case and add it to spectrum."""
    # TODO: consider accepting this config from CLI
    cov = coverage.Coverage(
        data_file=".afluent_coverage",
        auto_data=False,
        branch=True,
        config_file=False,
    )
    cov.start()
    yield
    cov.stop()
    pyfuncitem.session.session_spectrum[pyfuncitem.name] = {
        "coverage": {},
        "result": "notSet",
    }
    coverage_data = cov.get_data()
    for measured_file in coverage_data.measured_files():
        pyfuncitem.session.session_spectrum[pyfuncitem.name]["coverage"][
            measured_file
        ] = cov.get_data().lines(measured_file)
    cov.erase()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """Store the outcome of the test case as passed, failed, or skipped."""
    outcome = yield
    if outcome.get_result().when == "call":
        item.session.session_spectrum[item.name][
            "result"
        ] = outcome.get_result().outcome


def pytest_sessionfinish(session, exitstatus):
    """Perform the spectrum analysis if at least one test fails."""
    if not os.path.isdir("afluent_data"):
        os.mkdir("afluent_data")
    with open(
        "afluent_data/generated_spectrum.json", "w+", encoding="utf-8"
    ) as outfile:
        json.dump(session.session_spectrum, outfile)
    # Tests passed exit status
    if exitstatus == 0:
        exit_message = (fx.bold + fg.white + bg.green)(
            "\n\nAll tests passed no need to diagnose using AFLuent."
        )
        print(f"{exit_message}")
    # some tests failed exit status
    elif exitstatus == 1:
        exit_message = (fx.bold + fg.white + bg.red)(
            "\n\nFailing tests detected. Diagnosing using AFLuent..."
        )
        print(f"{exit_message}")
        full_spectrum = spectrum_parser.Spectrum(session.session_spectrum)
        with open("afluent_data/final_state.json", "w+", encoding="utf-8") as outfile:
            json.dump(full_spectrum.as_dict(), outfile)
        full_spectrum.print_report("tarantula")
