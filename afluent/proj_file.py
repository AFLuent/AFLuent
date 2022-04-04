"""Create object oriented structure for files carrying line coverage information."""
from typing import Dict

from afluent import tiebreak_generator

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
        self.cyclomatic_complexity_data: Dict[int, int] = {}
        self.logical_tiebreak_data: Dict[int, int] = {}
        self.enhanced_tiebreak_data: Dict[int, float] = {}

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
                    line_obj.tiebreakers[
                        "cyclomatic"
                    ] = self.cyclomatic_complexity_data[line_number]
                if self.logical_tiebreak_data:
                    line_obj.tiebreakers["logical"] = self.logical_tiebreak_data[
                        line_number
                    ]
                if self.enhanced_tiebreak_data:
                    line_obj.tiebreakers["enhanced"] = self.enhanced_tiebreak_data[
                        line_number
                    ]

                self.lines[line_number] = line_obj
            if test_result == "passed":
                self.lines[line_number].passed_by.append(test_case_name)
            elif test_result == "failed":
                self.lines[line_number].failed_by.append(test_case_name)
            elif test_result == "skipped":
                self.lines[line_number].skipped_by.append(test_case_name)
            else:
                raise Exception(f"Unknown test result for {test_case_name}")

    def get_cyclomatic_tiebreaker_dataset(self):
        """Use the file path to calculate cyclomatic complexity and update the data."""
        # set cyclomatic complexity to be enabled
        cc_generator = tiebreak_generator.CyclomaticComplexityGenerator(self.name)
        cc_generator.calculate_syntax_complexity()
        self.cyclomatic_complexity_data = cc_generator.data

    def get_logical_tiebreaker_dataset(self):
        """Use tiebreak generator to get the logical tiebreaker dataset."""
        mutant_density_generator = tiebreak_generator.LogicalTieBreaker(self.name)
        mutant_density_generator.calculate_mutant_density()
        self.logical_tiebreak_data = mutant_density_generator.score

    def get_enhanced_tiebreaker_dataset(self):
        """Use tiebreak generator to get the enhanced tiebreaker dataset."""
        generator = tiebreak_generator.EnhancedTieBreaker(self.name)
        generator.calculate_mutant_density()
        self.enhanced_tiebreak_data = generator.score

    def as_dict(self):
        """Return lines as a json writable dictionary."""
        data_dictionary = {}
        for line_num, line_obj in self.lines.items():
            data_dictionary[str(line_num)] = line_obj.as_dict()
        return data_dictionary
