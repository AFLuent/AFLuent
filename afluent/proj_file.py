"""Create object oriented structure for files carrying line coverage information."""
from afluent import line
from typing import Dict


class ProjFile:
    """Store coverage information about python files under test."""

    def __init__(self, name: str) -> None:
        """Initialize a ProjFile object.

        Args:
            name (str): name of the file under test
        """
        self.name = name
        self.lines: Dict[int, line.Line] = {}

    def update_file(self, covered_lines: list, test_result: str, test_case_name: str):
        for line_number in covered_lines:
            if line_number not in self.lines:
                self.lines[line_number] = line.Line(self.name, line_number)
            if test_result == "passed":
                self.lines[line_number].passed_by.append(test_case_name)
            elif test_result == "failed":
                self.lines[line_number].failed_by.append(test_case_name)
            elif test_result == "skipped":
                self.lines[line_number].skipped_by.append(test_case_name)
            else:
                raise Exception(f"Unknown test result for {test_case_name}")
