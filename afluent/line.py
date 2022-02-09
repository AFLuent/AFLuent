"""Create object oriented structure to keep track of line information."""

import math
from typing import List

TARAN = "tarantula"
OCHIAI = "ochiai"
DSTAR = "dstar"


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
        self.passed_by: List[str] = []
        self.failed_by: List[str] = []
        self.skipped_by: List[str] = []
        self.sus_scores = {
            TARAN: -1.0,
            OCHIAI: -1.0,
            DSTAR: -1.0,
        }

    def sus(self, method: str, passed_total: int, failed_total: int, power=3):
        """Calculate the suspiciousness score using the passed method.

        Args:
            method (str): name of the method to use
        """
        # TODO: refactor this a bit
        if method.lower() == TARAN:
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
        else:
            raise Exception("ERROR: unknown suspiciousness method")

    def sus_all(self, passed_total: int, failed_total: int, power=3):
        """Calculate the suspiciousness score for all available methods."""
        # TODO: refactor this a bit
        self.sus(TARAN, passed_total, failed_total)
        self.sus(OCHIAI, passed_total, failed_total)
        self.sus(DSTAR, passed_total, failed_total, power=power)

    def as_dict(self):
        """Return line information as json writable dictionary."""
        return self.__dict__

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
        # TODO: double check if this should happen
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
        # TODO: double check if this should happen
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
        # TODO: double check if this should happen
        if passed_cover + uncovered_failed == 0:
            return 999999999
        score = math.pow(failed_cover, power) / (passed_cover + uncovered_failed)
        return round(score, 4)
