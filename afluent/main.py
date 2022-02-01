import coverage
import json
import pytest


@pytest.hookimpl()
def pytest_sessionstart(session):
    session.session_spectrum = dict()


@pytest.hookimpl(hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem):
    cov = coverage.Coverage()
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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    if outcome.get_result().when == "call":
        item.session.session_spectrum[item.name][
            "result"
        ] = outcome.get_result().outcome


def pytest_sessionfinish(session, exitstatus):
    with open("spectrum_data.json", "w+") as outfile:
        json.dump(session.session_spectrum, outfile)
    print("Spectrum report generated...")
