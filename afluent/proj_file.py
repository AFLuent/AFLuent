"""Create object oriented structure for files carrying line coverage information."""
from typing import Any, Dict, List, Tuple
from afluent import line
import radon
import radon.complexity as cc


class ProjFile:
    """Store coverage information about python files under test."""

    def __init__(self, name: str) -> None:
        """Initialize a ProjFile object.

        Args:
            name (str): path of the file under test
        """
        self.name = name
        self.lines: Dict[int, line.Line] = {}
        self.complexity_data: List[Tuple[int, int, int]] = []

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
            # Line doesn't exist in the dataset, create new one
            if line_number not in self.lines:
                line_obj = line.Line(self.name, line_number)
                # get the complexity of the line
                line_obj.complexity = ProjFile.get_complexity_score(
                    line_number, self.complexity_data
                )
                self.lines[line_number] = line_obj
            if test_result == "passed":
                self.lines[line_number].passed_by.append(test_case_name)
            elif test_result == "failed":
                self.lines[line_number].failed_by.append(test_case_name)
            elif test_result == "skipped":
                self.lines[line_number].skipped_by.append(test_case_name)
            else:
                raise Exception(f"Unknown test result for {test_case_name}")

    def get_complexity_dataset(self):
        """Use the file path to calculate complexity and update the data."""
        with open(self.name, "r", encoding="utf-8") as infile:
            file_string = infile.read()
            complexity_data = cc.sorted_results(cc.cc_visit(file_string), cc.LINES)
        # reassemble complexity data to follow this format
        # List(Tuple(line_start:int, line_end:int, complexity_score:int))
        cc_lines = []
        for item in complexity_data:
            # Check if the current item is a Function and add it's information
            if isinstance(item, radon.visitors.Function):
                cc_lines.append((item.lineno, item.endline, item.complexity))
        self.complexity_data = cc_lines

    def as_dict(self):
        """Return lines as a json writable dictionary."""
        data_dictionary = {}
        for line_num, line_obj in self.lines.items():
            data_dictionary[str(line_num)] = line_obj.as_dict()
        return data_dictionary

    @staticmethod
    def get_complexity_score(line_num, dataset) -> int:
        """Searches for the correct line range in the dataset and return the
        complexity score.add()

        Args:
            line_num (int): number of the line being searched for
            dataset (List[Tuple[int, int, int]]): Dataset of line number ranges
            and their complexity

        Returns:
            int: the complexity of the line or 0 if the line wasn't found
        """
        if not dataset:
            return 0
        # TODO: refactor to use binary search
        for line_range in dataset:
            if line_num >= line_range[0] and line_num <= line_range[1]:
                return line_range[2]
        return 0
