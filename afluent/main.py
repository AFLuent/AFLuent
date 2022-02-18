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
# TODO: figure out what else


def pytest_addoption(parser, pluginmanager):
    """Add AFLuent command line group and arguments to accept."""
    afluent_group = parser.getgroup("afluent", "Automated Fault Localization (AFLuent)")
    afluent_group.addoption(
        "--afl-debug",
        "--afl",
        dest="afl_enable",
        action="store_true",
        default=False,
        help="Enable AFLuent",
    )
    afluent_group.addoption(
        "--tarantula",
        dest="afl_methods",
        action="append_const",
        const="tarantula",
        help="Enable debugging using Tarantula",
    )
    afluent_group.addoption(
        "--ochiai",
        dest="afl_methods",
        action="append_const",
        const="ochiai",
        help="Enable debugging using Ochiai",
    )
    afluent_group.addoption(
        "--dstar",
        dest="afl_methods",
        action="append_const",
        const="dstar",
        help="Enable debugging using Dstar",
    )
    afluent_group.addoption(
        "--dstar-pow",
        dest="dstar_pow",
        default=3,
        action="store",
        type=int,
        help="Power to use when calculating Dstar score, default to 3",
    )
    afluent_group.addoption(
        "--afl-results",
        dest="results_num",
        default=20,
        action="store",
        type=int,
        help="Number of results to display in the score report , default to 20",
    )
    afluent_group.addoption(
        "--afl-ignore",
        dest="afl_ignore",
        action="extend",
        nargs="*",
        type=str,
        help="Names of files/directories to ignore when calculating coverage for AFLuent.",
    )


def pytest_cmdline_main(config):
    """Check if AFLuent is enabled and register the plugin object."""
    # check if the argument to enable afluent exists and create the object with
    # the passed configuration
    # TODO: check if other plugins that rely on coverage are registered
    if config.getoption("afl_enable"):
        plugin = Afluent()
        config.pluginmanager.register(plugin, "Afluent")
    else:
        print(
            (fx.bold + fg.white + bg.orange)(
                "\nAFLuent is disabled, report will not be produced."
            )
        )
        print()


class Afluent:
    def __init__(self):
        self.enabled = False

    @pytest.hookimpl()
    def pytest_sessionstart(self, session):
        """Create a session variable as empty dictionary to store coverage."""
        session.session_spectrum = {}

    @pytest.hookimpl(hookwrapper=True)
    def pytest_pyfunc_call(self, pyfuncitem):
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
    def pytest_runtest_makereport(self, item):
        """Store the outcome of the test case as passed, failed, or skipped."""
        outcome = yield
        if outcome.get_result().when == "call":
            item.session.session_spectrum[item.name][
                "result"
            ] = outcome.get_result().outcome

    def pytest_sessionfinish(self, session, exitstatus):
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
            with open(
                "afluent_data/final_state.json", "w+", encoding="utf-8"
            ) as outfile:
                json.dump(full_spectrum.as_dict(), outfile)
            full_spectrum.print_report("tarantula")
