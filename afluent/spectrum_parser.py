"""Implement parsing and reassembling functions for coverage data."""

from typing import Dict, List

from console import fg, bg, fx  # type: ignore[import]
from afluent import proj_file, line

METHOD_NAMES = ["tarantula", "ochiai", "dstar"]

PALETTE = {
    "severe": fg.white + fx.bold + bg.lightred,
    "risky": fg.white + fx.bold + bg.i208,
    "mild": fg.white + fx.bold + bg.yellow,
    "safe": fg.white + fx.bold + bg.green,
    "location_line": fg.white,
}


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

    def generate_report(self, method: str, max_items=-1) -> str:
        """Generate and pretty print the AFL report."""
        overall_text = ""
        if method not in METHOD_NAMES:
            raise Exception(f"ERROR: Invalid method name {method}")
        sorted_lines = self.generate_rankings(method)
        if max_items > 0:
            sorted_lines = sorted_lines[:max_items]
        # pylint: disable=C0200
        for line_index in range(0, len(sorted_lines)):
            line_obj = sorted_lines[line_index]
            line_location, sus_score = line_obj.sus_text(method)
            severity_text = Spectrum.apply_severity(
                line_location,
                method,
                sus_score,
                line_index,
                max_items,
            )
            overall_text += f"{severity_text}\n"
        return overall_text

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
        """Iterate through reassembeled data and calculate the suspiciousness of every line."""
        for _, current_file in self.reassembled_data.items():
            for _, current_line in current_file.lines.items():
                # TODO: add the power argument as passed from user
                current_line.sus_all(self.totals["passed"], self.totals["failed"])

    def as_dict(self):
        """Return the spectrum information as a JSON writable dictionary."""
        data_dict = {}
        for file_name, file_obj in self.reassembled_data.items():
            data_dict[file_name] = file_obj.as_dict()

        return data_dict

    def generate_rankings(self, method: str) -> List[line.Line]:
        """Return a list of line objects ranked from the most to least suspicious.

        Args:
            method (str): name of the suspiciousness score to use for sorting
        """
        # Gather up all the line objects in one list
        all_lines: List[line.Line] = []
        for file_obj in self.reassembled_data.values():
            all_lines.extend(file_obj.lines.values())
        all_lines.sort(key=lambda x: x.sus_scores[method], reverse=True)
        return all_lines

    def print_report(self, method: str):
        """Print a nicely formatted suspiciousness report using the chosen method."""
        if method not in METHOD_NAMES:
            raise Exception(f"ERROR: Invalid method name {method}")
        print()
        header_text = (
            f"{'====================== AFLuent Report =====================': ^15}"
        )
        print(f"{header_text}")
        print(self.generate_report(method))

    @staticmethod
    def apply_severity(
        line_location: str, method: str, sus_score: float, rank: int, out_of: int
    ) -> str:
        """Return a formatted/color coded string that shows the line suspiciousness score.

        Args:
            line_location (str): a string representation of the line location
            method (str): name of the suspiciousness method used
            sus_score (float): suspiciousness score of the line
            rank (int): the rank of this line in the sorted list
            out_of (int): length of the sorted list
        """
        string_representation = f"{PALETTE['location_line'](line_location)}\t"
        format_function = Spectrum.calculate_severity(method, sus_score, rank, out_of)
        string_representation += f"{format_function(str(sus_score))}"
        return string_representation

    @staticmethod
    def calculate_severity(method: str, sus_score: float, rank: int, out_of: int):
        """Return a function to format strings according to score severity.

        Args:
            method (str): name of the suspiciousness method used
            sus_score (float): suspiciousness score of the line
            rank (int): the rank of this line in the sorted list
            out_of (int): length of the sorted list
        """
        if sus_score <= 0:
            return PALETTE["safe"]
        if (method in ["tarantula", "ochiai"]) and sus_score == 1:
            return PALETTE["severe"]
        # TODO: might need updated
        if method == "dstar" and sus_score == 999999999:
            return PALETTE["severe"]
        if rank / out_of <= 0.2:
            return PALETTE["risky"]
        return PALETTE["mild"]
