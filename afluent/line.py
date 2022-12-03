"""Create object oriented structure to keep track of line information."""

import math
from typing import List

# Scores:   # New Formula
TARAN = "tarantula"
OCHIAI = "ochiai"
OCHIAI2 = "ochiai2"
DSTAR = "dstar"
OP2 = "op2"


# Tiebreakers
RANDOM = "random"
CYCLOMATIC = "cyclomatic"
LOGICAL = "logical"
ENHANCED = "enhanced"


# pylint: disable=R0902
class Line:
    """Implement the line object and suspiciousness calculation."""

    def __init__(self, file_path: str, line_num: int) -> None:
        """Initialize a line object.

        Args:
            file_path (str): Path to the file where the line exists
            line_num (int): number of the line in the file
        """
        self.path = file_path
        self.number = line_num
        self.passed_by: List[
            str
        ] = []  # List of test functions that ran this Line and passed
        self.failed_by: List[str] = []  # the names of those that failed
        self.skipped_by: List[str] = []
        self.sus_scores = {  # default values for our formulas # New Formula
            TARAN: -1.0,
            OCHIAI: -1.0,
            DSTAR: -1.0,
            OCHIAI2: -1.0,
            OP2: -1.0,
        }
        self.tiebreakers = {
            CYCLOMATIC: 0.0,
            LOGICAL: 0.0,
            ENHANCED: 0.0,
            # *SHOULD ALWAYS STAY ZERO
            RANDOM: 0.0,
        }

    def sus(self, method: str, passed_total: int, failed_total: int, power=3): # New Formula
        """Calculate the suspiciousness score using the passed method.

        Args:
            method (str): name of the method to use
        """
        if method.lower() == TARAN:  # if the method is tarantula, do this
            self.sus_scores[TARAN] = Line.tarantula(
                len(self.failed_by),
                len(self.passed_by),
                passed_total,
                failed_total,
            )
        elif method.lower() == OCHIAI:
            self.sus_scores[OCHIAI] = Line.ochiai(
                len(self.failed_by), len(self.passed_by), failed_total
            )
        elif method.lower() == DSTAR:
            self.sus_scores[DSTAR] = Line.dstar(
                len(self.failed_by), len(self.passed_by), failed_total, power
            )
        elif method.lower() == OCHIAI2:
            self.sus_scores[OCHIAI2] = Line.ochiai2(
                len(self.failed_by),
                len(self.passed_by),
                passed_total,
                failed_total,
            )
        elif method.lower() == OP2:
            self.sus_scores[OP2] = Line.op2(
                len(self.failed_by),
                len(self.passed_by),
                passed_total,
            )
        else:
            raise Exception("ERROR: unknown suspiciousness method")

    def sus_all( # New Formula
        self, passed_total: int, failed_total: int, power=3
    ):  # use all formulas
        """Calculate the suspiciousness score for all available methods."""
        self.sus(TARAN, passed_total, failed_total)
        self.sus(OCHIAI, passed_total, failed_total)
        self.sus(DSTAR, passed_total, failed_total, power=power)
        self.sus(OCHIAI2, passed_total, failed_total)
        self.sus(OP2, passed_total, failed_total)

    def as_dict(self):  # give me the representation of this object as a dictionary
        """Return line information as json writable dictionary."""
        return self.__dict__

    def as_csv(self):  # give me the representation of this object as a csv # New Formula
        """Return line information as csv writable list."""
        return [
            self.path,
            self.number,
            self.sus_scores[TARAN],
            self.sus_scores[OCHIAI],
            self.sus_scores[OCHIAI2],
            self.sus_scores[DSTAR],
            self.sus_scores[OP2],
        ]

    def sus_text(self, methods):
        """Return a tuple of string of line information and score value."""
        sus_list = []
        for method_name in methods:
            sus_list.append(self.sus_scores[method_name])
        return (self.path, self.number, sus_list)

    @staticmethod
    def tarantula(
        failed_cover: int, passed_cover: int, total_passed: int, total_failed: int
    ) -> float:
        """Calculate suspiciousness score using the tarantula approach.

        Args:
            failed_cover (int): total number of failed test cases that cover the line
            passed_cover (int): total number of passed test cases that cover the line
            total_passed (int): total number of passed test cases
            total_failed (int): total number of failed test cases

        Returns:
            float: suspiciousness score using tarantula
        """
        if total_passed == 0:
            return 1
        if total_failed == 0:
            return 0
        score = (failed_cover / total_failed) / (
            (passed_cover / total_passed) + (failed_cover / total_failed)
        )
        return round(score, 4)

    @staticmethod
    def ochiai(failed_cover: int, passed_cover: int, total_failed: int) -> float:
        """Calculate suspiciousness score using the ochiai approach.

        Args:
            failed_cover (int): total number of failed test cases that cover the line
            passed_cover (int): total number of passed test cases that cover the line
            total_failed (int): total number of failed test cases

        Returns:
            float: suspiciousness score using ochiai
        """
        if total_failed == 0 or failed_cover == 0:
            return 0
        score = failed_cover / math.sqrt(total_failed * (passed_cover + failed_cover))
        return round(score, 4)

    @staticmethod
    def dstar(
        failed_cover: int, passed_cover: int, total_failed: int, power=3
    ) -> float:
        """Calculate suspiciousness score using the dstar approach.

        Args:
            failed_cover (int): total number of failed test cases that cover the line
            passed_cover (int): total number of passed test cases that cover the line
            total_failed (int): total number of failed test cases
            power (int, optional): Power to use in the equation. Defaults to 3.

        Returns:
            float: suspiciousness score using dstar
        """
        uncovered_failed = total_failed - failed_cover
        if passed_cover + uncovered_failed == 0:
            return float("inf")
        score = math.pow(failed_cover, power) / (passed_cover + uncovered_failed)
        return round(score, 4)

    # New Formula
    @staticmethod
    def op2(failed_cover: int, passed_cover: int, total_passed: int) -> float:
        """Calculate suspiciousness score using the op2 approach.

        Args:
            failed_cover (int): total number of failed test cases that cover the line
            passed_cover (int): total number of passed test cases that cover the line
            total_passed (int): total number of passed test cases

        Returns:
            float: suspiciousness score using op2
        """
        score = failed_cover - (passed_cover / (total_passed + 1))
        return round(score, 4)

    @staticmethod
    def ochiai2(
        failed_cover: int, passed_cover: int, total_passed: int, total_failed: int
    ) -> float:
        """Calculate suspiciousness score using the ochiai2 approach.

        Args:
            failed_cover (int): total number of failed test cases that cover the line
            passed_cover (int): total number of passed test cases that cover the line
            total_passed (int): total number of passed test cases
            total_failed (int): total number of failed test cases

        Returns:
            float: suspiciousness score using ochiai2
        """
        # !DIVISION BY ZERO WHEN
        # ?If there are no tests that cover the statement: not happening, we're
        # only looking at covered statements to begin with
        # !If there are no tests that do not cover the statement: UNSURE
        # ?If the total failed is zero: not possible, for AFLuent to run, there
        # has to be at least one failure
        # ?If total passed is zero => everything is suspicious, no info really
        passed_uncover = total_passed - passed_cover
        failed_uncover = total_failed - failed_cover
        total_cover = passed_cover + failed_cover
        total_uncover = passed_uncover + failed_uncover
        if total_passed == 0:
            return 1.0
        if total_uncover == 0:
            return 0
        if total_failed == 0:
            return 0
        if total_cover == 0:
            return 0
        numerator = failed_cover * passed_uncover
        denominator = math.sqrt(
            total_cover * total_uncover * total_failed * total_passed
        )
        score = numerator / denominator
        return round(score, 4)
