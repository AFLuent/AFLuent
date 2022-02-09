"""Define Pytest Hooks that run AFLuent."""

import coverage  # type: ignore[import]
import pytest  # type: ignore[import]
import json
from afluent import spectrum_parser


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
    with open("generated_spectrum.json", "w+", encoding="utf-8") as outfile:
        json.dump(session.session_spectrum, outfile)
        print("report exported to json")
    # Tests passed exit status
    if exitstatus == 0:
        print("\nAll tests passed no need to diagnose using AFLuent.")
    # some tests failed exit status
    elif exitstatus == 1:
        print("\nFailing tests detected. Diagnosing using AFLuent...")
        full_spectrum = spectrum_parser.Spectrum(session.session_spectrum)
        full_spectrum.generate_report()
        # TODO: add the rest of the spectrum calls
        print("Spectrum report generated...")
