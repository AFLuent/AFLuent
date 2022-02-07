"""Create object oriented structure for files carrying line coverage information."""
from typing import Dict
from afluent import line


class ProjFile:
    """Store coverage information about python files under test."""

    def __init__(self, name: str) -> None:
        """Initialize a ProjFile object.

        Args:
            name (str): name of the file under test
        """
        self.name = name
        self.lines: Dict[int, line.Line] = {}

    def update_file(
        self, covered_lines: list[int], test_result: str, test_case_name: str
    ):
        """Update lines information in a file object.

        Args:
            covered_lines (list[int]): list of integer values of the lines covered
            test_result (str): one of three possible values `passed` `failed` or `skipped`
            test_case_name (str): name of the test case being ran

        Raises:
            Exception: when a result is not one of the three possible values
        """
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

    def as_dict(self):
        """Return lines as a json writable dictionary."""
        data_dictionary = {}
        for line_num, line_obj in self.lines.items():
            data_dictionary[str(line_num)] = line_obj.as_dict()
        return data_dictionary
