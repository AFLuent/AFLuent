"""Implement parsing and reassembling functions for coverage data."""

import csv
import json
import random

from typing import Any, Dict, List, Tuple

from console import fg, bg, fx  # type: ignore[import]
from tabulate import tabulate
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

    def __init__(self, config, dstar_pow=3, complexity=False) -> None:
        """Initialize a spectrum object.

        Args:
            config (dict): per-test coverage information
            dstar_pow (int): power to use when calculating scores using dstar
        """
        self.config = config
        self.reassembled_data: Dict[str, proj_file.ProjFile] = {}
        self.sorted_lines: List[line.Line] = []
        self.totals = {"passed": 0, "failed": 0, "skipped": 0}
        self.dstar_pow = dstar_pow
        self.complexity = complexity
        self.reassemble()
        self.calculate_sus()

    def generate_report(
        self, methods: List[str], max_items=-1
    ) -> List[Tuple[Any, ...]]:
        """Generate a list of tuples containing report information."""
        report_list = []
        # Sort the lines based on the first method name used in the list
        sorted_lines = self.generate_rankings(methods[0])
        if max_items > 0:
            sorted_lines = sorted_lines[:max_items]
        # pylint: disable=C0200
        for line_index in range(0, len(sorted_lines)):
            line_obj = sorted_lines[line_index]
            line_path, line_number, sus_scores = line_obj.sus_text(methods)
            line_path = f"{PALETTE['location_line'](line_path)}"
            line_number = f"{PALETTE['location_line'](str(line_number))}"
            current_row = [line_path, line_number]
            format_function = Spectrum.calculate_severity(
                methods[0], sus_scores[0], line_index, len(sorted_lines)
            )
            for method_score in sus_scores:
                current_row.append(f"{format_function(str(method_score))}")
            # TODO: remove complexity from display
            current_row.append(str(line_obj.complexity))
            report_list.append(tuple(current_row))
        return report_list

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
                    # Initialize a new object of one doesn't already exist
                    file_obj = proj_file.ProjFile(file_name)
                    if self.complexity:
                        # calculate it's complexity dataset
                        file_obj.get_cyclomatic_complexity_dataset()
                    self.reassembled_data[file_name] = file_obj
                self.reassembled_data[file_name].update_file(
                    lines_covered, test_result, test_case_name
                )

    def calculate_sus(self):
        """Iterate through reassembeled data and calculate the suspiciousness of every line."""
        for _, current_file in self.reassembled_data.items():
            for _, current_line in current_file.lines.items():
                current_line.sus_all(
                    self.totals["passed"], self.totals["failed"], power=self.dstar_pow
                )

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
        # Introduce some randomness before sorting
        random.shuffle(all_lines)
        all_lines.sort(key=lambda x: (x.sus_scores[method], x.complexity), reverse=True)
        # store the sorted list as an attribute
        self.sorted_lines = all_lines
        return all_lines

    def print_report(self, methods: List[str], items_num: int):
        """Print a nicely formatted suspiciousness report using the chosen method."""
        for method_name in methods:
            if method_name not in METHOD_NAMES:
                raise Exception(f"ERROR: Invalid method name {method_name}")
        print()
        header_text = "============================ AFLuent Report ==============================="
        table_headers = [
            PALETTE["location_line"]("File Path"),
            PALETTE["location_line"]("Line Number"),
        ]
        for method_name in methods:
            table_headers.append(PALETTE["location_line"](f"{method_name} Score"))
        # TODO: remove this header
        table_headers.append(PALETTE["location_line"]("Complexity"))
        print(f"{PALETTE['location_line'](header_text)}")
        print(
            tabulate(
                self.generate_report(methods, max_items=items_num),
                headers=table_headers,
                tablefmt="rst",
            )
        )

    def store_report(self, report_type):
        """Create and store a report file."""
        if report_type == "json":
            data_dict = {}
            lines_list = list(map(lambda x: x.as_dict(), self.sorted_lines))
            data_dict["ranking"] = lines_list
            with open("afluent_report.json", "w+", encoding="utf-8") as outfile:
                json.dump(data_dict, outfile, indent=4)
        elif report_type == "csv":
            header = [
                "Path",
                "Line number",
                "Tarantula Score",
                "Ochiai Score",
                "Dstar Score",
            ]
            with open("afluent_report.csv", "w+", encoding="utf-8") as outfile:
                csv_writer = csv.writer(outfile)
                csv_writer.writerow(header)
                lines_list = list(map(lambda x: x.as_csv(), self.sorted_lines))
                csv_writer.writerows(lines_list)

        else:
            raise Exception(f"Error:Unknown report type {report_type}.")

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
