"""Define Pytest Hooks that run AFLuent."""

from gettext import install
import json

import coverage  # type: ignore[import]
import pytest  # type: ignore[import]
from console import bg, fg, fx  # type: ignore[import]

from afluent import spectrum_parser

from pprint import pprint

WARNING = fx.bold + fg.white + bg.orange
ERROR = fx.bold + fg.white + bg.red
VALID = fx.bold + fg.white + bg.green

CONFLICTING_PLUGINS = ["pytest_cov"]


def pytest_addoption(parser):
    """Add AFLuent command line group and arguments to accept."""
    # TODO: figure out what other arguments are needed
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
        help="Enable fault localization using Tarantula",
    )
    afluent_group.addoption(
        "--ochiai",
        dest="afl_methods",
        action="append_const",
        const="ochiai",
        help="Enable fault localization using Ochiai",
    )
    afluent_group.addoption(
        "--ochiai2",
        dest="afl_methods",
        action="append_const",
        const="ochiai2",
        help="Enable fault localization using Ochiai2",
    )
    afluent_group.addoption(
        "--dstar",
        dest="afl_methods",
        action="append_const",
        const="dstar",
        help="Enable fault localization using Dstar",
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
        help="File patterns to ignore when calculating coverage for AFLuent (example: tests/*).",
    )
    afluent_group.addoption(
        "--report",
        dest="report_type",
        action="store",
        default=None,
        type=str,
        choices=["json", "csv", "eval"],
        help="Store report after AFLuent run.",
    )
    afluent_group.addoption(
        "--per-test-report",
        dest="per_test",
        action="store_true",
        help="Get per test case coverage report.",
    )
    afluent_group.addoption(
        "--tiebreaker",
        dest="tiebreaker",
        action="store",
        default="random",
        type=str,
        choices=["random", "cyclomatic", "logical", "enhanced"],
        help="Type of tie breaking approach.",
    )


def pytest_cmdline_main(config):
    """Check if AFLuent is enabled and register the plugin object."""
    # check if the argument to enable afluent exists and create the object with
    # the passed configuration
    installed_plugins = config.pluginmanager.list_name_plugin()
    for plugin_name, _ in installed_plugins:
        if plugin_name in CONFLICTING_PLUGINS:
            print(
                WARNING(
                    f"\n{plugin_name} plugin conflicts with AFLuent, consider disabling\n"
                    + "it for this session to get the most accurate fault localization results.\n\n"
                )
            )

    if config.getoption("afl_enable"):
        # Check if exit after failure is enabled and display warning message
        if config.getoption("--maxfail"):
            print(
                WARNING(
                    "\nExit after failure detected. AFLuent gives more "
                    + "accurate results if the full test suite was ran.\n\n"
                    + "Consider removing `-x` and/or `--maxfail` from CLI arguments."
                )
            )
            print()
        plugin = Afluent(config)
        config.pluginmanager.register(plugin, "Afluent")
    else:
        print(
            WARNING(
                "\nAFLuent is disabled. Enable AFLuent by adding --afl or --afl-debug to the test command."
            )
        )
        print()


class Afluent:
    """Contain all the functionalities and hooks of the AFLuent plugin."""

    # pylint: disable=R0913, R0902
    def __init__(self, pytest_config):
        """Initialize a plugin object with it's pytest hooks."""
        self.methods = pytest_config.getoption("afl_methods")
        # if no methods were passed, include all of them
        if not self.methods:
            self.methods = ["dstar", "tarantula", "ochiai", "ochiai2"]
        self.dstar_pow = pytest_config.getoption("dstar_pow")
        self.results_num = pytest_config.getoption("results_num")
        self.ignore = pytest_config.getoption("afl_ignore")
        self.report = pytest_config.getoption("report_type")
        self.per_test = pytest_config.getoption("per_test")
        self.tiebreaker = pytest_config.getoption("tiebreaker")
        if self.report == "eval":
            self.eval_mode = True
        else:
            self.eval_mode = False
        self.session_spectrum = {}
        self.cov = coverage.Coverage(
            data_file=None,
            auto_data=False,
            branch=True,
            config_file=False,
            omit=self.ignore,
        )

    @pytest.hookimpl(hookwrapper=True)
    def pytest_pyfunc_call(self, pyfuncitem):
        """Calculate the coverage of each test case and add it to spectrum."""
        try:
            self.cov.start()
            yield
            self.cov.stop()
            coverage_data = self.cov.get_data()
            self.session_spectrum[pyfuncitem.name] = {
                "coverage": {},
                "result": "notSet",
            }
            for measured_file in coverage_data.measured_files():
                self.session_spectrum[pyfuncitem.name]["coverage"][
                    measured_file
                ] = self.cov.get_data().lines(measured_file)
        except coverage.exceptions.CoverageWarning:
            pass
        self.cov.erase()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item):
        """Store the outcome of the test case as passed, failed, or skipped."""
        outcome = yield
        if outcome.get_result().when == "call" and item.name in self.session_spectrum:
            self.session_spectrum[item.name]["result"] = outcome.get_result().outcome

    def pytest_sessionfinish(self, exitstatus):
        """Perform the spectrum analysis if at least one test fails."""
        # Store generated json
        if self.per_test:
            with open(
                "afluent_per_test_report.json", "w+", encoding="utf-8"
            ) as outfile:
                json.dump(self.session_spectrum, outfile, indent=4)
        # Tests passed, exit status is 0
        if exitstatus == 0:
            exit_message = VALID(
                "\n\nAll tests passed, no need to diagnose using AFLuent."
            )
            print(f"{exit_message}")
        # some tests failed exit status
        elif exitstatus == 1:
            exit_message = ERROR(
                "\n\nFailing tests detected. Diagnosing using AFLuent..."
            )
            print(f"{exit_message}")
            full_spectrum = spectrum_parser.Spectrum(
                self.session_spectrum,
                dstar_pow=self.dstar_pow,
                tiebreaker=self.tiebreaker,
                eval_mode=self.eval_mode,
            )
            full_spectrum.print_report(self.methods, self.results_num)
            if self.report:
                print(f"Storing {self.report} report...")
                full_spectrum.store_report(self.report)
