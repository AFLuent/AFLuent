"""Create object oriented structure for files carrying line coverage information."""
from typing import Any, Dict, List, Tuple

from afluent import complexity_generator

from afluent import line


class ProjFile:
    """Store coverage information about python files under test."""

    def __init__(self, name: str) -> None:
        """Initialize a ProjFile object.

        Args:
            name (str): path of the file under test
        """
        self.name = name
        self.lines: Dict[int, line.Line] = {}
        self.cyclomatic_complexity_data: List[Tuple[int, int, int]] = []
        self.syntax_complexity_data: Dict[int, List[Dict[str, Any]]] = {}

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
                if self.cyclomatic_complexity_data:
                    # get the complexity of the line
                    line_obj.c_complexity = ProjFile.get_cyclomatic_complexity_score(
                        line_number, self.cyclomatic_complexity_data
                    )
                # TODO: implement how syntax complexity should be retrieved
                # if self.syntax_complexity_data:

                self.lines[line_number] = line_obj
            if test_result == "passed":
                self.lines[line_number].passed_by.append(test_case_name)
            elif test_result == "failed":
                self.lines[line_number].failed_by.append(test_case_name)
            elif test_result == "skipped":
                self.lines[line_number].skipped_by.append(test_case_name)
            else:
                raise Exception(f"Unknown test result for {test_case_name}")

    def get_cyclomatic_complexity_dataset(self):
        """Use the file path to calculate complexity and update the data."""
        # set cyclomatic complexity to be enabled
        cc_generator = complexity_generator.CyclomaticComplexityGenerator(self.name)
        cc_generator.calculate_syntax_complexity()
        self.cyclomatic_complexity_data = cc_generator.data

    def get_syntax_complexity_dataset(self):
        s_generator = complexity_generator.SyntaxtComplexityGenerator(self.name)
        s_generator.calculate_syntax_complexity()
        # TODO: change what gets used here
        self.syntax_complexity_data = s_generator.data

    def as_dict(self):
        """Return lines as a json writable dictionary."""
        data_dictionary = {}
        for line_num, line_obj in self.lines.items():
            data_dictionary[str(line_num)] = line_obj.as_dict()
        return data_dictionary

    @staticmethod
    def get_cyclomatic_complexity_score(line_num, dataset) -> int:
        """Search for the correct line range in the dataset and return the complexity score.

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
            if line_range[0] <= line_num <= line_range[1]:
                return line_range[2]
        return 0
