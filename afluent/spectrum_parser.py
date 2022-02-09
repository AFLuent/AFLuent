"""Implement parsing and reassembling functions for coverage data."""

from typing import Dict

from afluent import proj_file


class Spectrum:
    """Store all the information for individual files and lines coverage."""

    def __init__(self, config) -> None:
        """Initialize a spectrum object.

        Args:
            config (dict): per-test coverage information
        """
        self.config = config
        self.reassembled_data: Dict[str, proj_file.ProjFile] = {}
        self.totals = {"passed": 0, "failed": 0, "skipped": 0}
        self.reassemble()
        self.calculate_sus()

    def generate_report(self):
        """Generate and pretty print the AFL report."""
        print(f"here is the report {self.reassembled_data}")

    def reassemble(self):
        """Reassemble the coverage information on a file and line basis."""
        # Config is empty, return nothing
        if not self.config:
            return
        # iterate through every test case in the spectrum report
        for test_case_name, spectrum_dict in self.config.items():
            test_result = spectrum_dict["result"]
            # increment the totals
            self.totals[test_result] += 1
            for file_name, lines_covered in spectrum_dict["coverage"].items():
                if file_name not in self.reassembled_data:
                    self.reassembled_data[file_name] = proj_file.ProjFile(file_name)
                self.reassembled_data[file_name].update_file(
                    lines_covered, test_result, test_case_name
                )

    def calculate_sus(self):
        """Iterate through reassembeled data and calculate the suspiciousness of
        every line."""
        for file_name, current_file in self.reassembled_data.items():
            for line_number, current_line in current_file.lines.items():
                # TODO: add the power argument as passed from user
                current_line.sus_all(self.totals["passed"], self.totals["failed"])

    def as_dict(self):
        """Return the spectrum information as a JSON writable dictionary."""
        data_dict = {}
        for file_name, file_obj in self.reassembled_data.items():
            data_dict[file_name] = file_obj.as_dict()

        return data_dict
