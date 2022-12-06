"""Implement parsing and reassembling functions for coverage data."""

import csv
import json
import random

from typing import Any, Dict, List, Tuple

from console import fg, bg, fx  # type: ignore[import]
from tabulate import tabulate
from afluent import proj_file, line


METHOD_NAMES = [ # New formula
    "tarantula",
    "ochiai",
    "ochiai2",
    "dstar",
    "op2",
    "barinel",
    "jaccard",
    "kulczynski",
    "kulczynski2",
    "mccon",
    "minus",
    # "zoltar",
]  # formula names
TIEBREAKERS = ["random", "cyclomatic", "logical", "enhanced"]  # tiebreaking approaches

PALETTE = {
    "severe": fg.white + fx.bold + bg.lightred,
    "risky": fg.white + fx.bold + bg.i208,
    "mild": fg.white + fx.bold + bg.yellow,
    "safe": fg.white + fx.bold + bg.green,
    "location_line": fg.white,
}


class Spectrum:
    """Store all the information for individual files and lines coverage."""

    def __init__(
        self, config, dstar_pow=3, tiebreaker="random", eval_mode=False
    ) -> None:
        """Initialize a spectrum object.

        Args:
            config (dict): per-test coverage information
            dstar_pow (int): power to use when calculating scores using dstar
        """
        self.config = config
        # dictionary of names of files that map to a ProjFile
        self.reassembled_data: Dict[str, proj_file.ProjFile] = {}
        self.sorted_lines: List[line.Line] = []
        self.totals = {"passed": 0, "failed": 0, "skipped": 0}
        self.dstar_pow = dstar_pow
        self.tiebreaker = tiebreaker
        self.eval_mode = eval_mode
        self.reassemble()
        self.calculate_sus()

    def generate_report(
        self, methods: List[str], max_items=-1
    ) -> List[Tuple[Any, ...]]:
        """Generate a list of tuples containing report information."""
        report_list = []
        # Gather up all the line objects in one list
        all_lines: List[line.Line] = []
        for file_obj in self.reassembled_data.values():
            all_lines.extend(file_obj.lines.values())
        # Sort the lines based on the first method name used in the list
        sorted_lines = Spectrum.generate_rankings(
            all_lines, methods[0], tiebreaker=self.tiebreaker
        )
        # store as an instance variable to generate reports later
        self.sorted_lines = sorted_lines
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
                    if self.eval_mode:
                        # populate all tieberaker datasets
                        file_obj.get_logical_tiebreaker_dataset()
                        file_obj.get_enhanced_tiebreaker_dataset()
                        file_obj.get_cyclomatic_tiebreaker_dataset()
                    elif self.tiebreaker == "logical":
                        # collect logical tiebreak dataset only
                        file_obj.get_logical_tiebreaker_dataset()
                    elif self.tiebreaker == "enhanced":
                        # collect enhanced tiebreak dataset only
                        file_obj.get_enhanced_tiebreaker_dataset()
                    elif self.tiebreaker == "cyclomatic":
                        # collect cyclometer dataset only
                        file_obj.get_cyclomatic_tiebreaker_dataset()
                    # * Random tiebreaker doesn't need dataset
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
            header = [ # New formula
                "Path",
                "Line number",
                "Tarantula Score",
                "Ochiai Score",
                "Ochiai2 Score",
                "Dstar Score",
                "Op2 Score",
                "Barinel Score",
                "Jaccard Score",
                "Kulczynski Score",
                "Kulczynski2 Score",
                "McCon Score",
                "Minus Score",
                # "Zoltar Score",
            ]
            with open("afluent_report.csv", "w+", encoding="utf-8") as outfile:
                csv_writer = csv.writer(outfile)
                csv_writer.writerow(header)
                lines_list = list(map(lambda x: x.as_csv(), self.sorted_lines))
                csv_writer.writerows(lines_list)

        elif report_type == "eval":
            self.produce_full_eval_report()
        else:
            raise Exception(f"Error:Unknown report type {report_type}.")

    # pylint: disable=W0640
    def produce_full_eval_report(self):
        """Produce csv reports for all equation tie breaker combinatoins."""
        for method in METHOD_NAMES:
            for tiebreaker in TIEBREAKERS:
                ranked_lines = Spectrum.generate_rankings(
                    self.sorted_lines, method, tiebreaker=tiebreaker
                )
                file_to_store = f"{method}_{tiebreaker}_report.csv"
                header = [
                    "Path",
                    "Line number",
                    f"{method} score",
                    f"{tiebreaker} score",
                ]
                with open(file_to_store, "w+", encoding="utf-8") as outfile:
                    csv_writer = csv.writer(outfile)
                    csv_writer.writerow(header)
                    lines_list = list(
                        map(
                            lambda x: [
                                x.path,
                                x.number,
                                x.sus_scores[method],
                                x.tiebreakers[tiebreaker],
                            ],
                            ranked_lines,
                        )
                    )
                    csv_writer.writerows(lines_list)

    @staticmethod
    def generate_rankings(
        all_lines: List[line.Line], method: str, tiebreaker="random"
    ) -> List[line.Line]:
        """Return a list of line objects ranked from the most to least suspicious.

        Args:
            method (str): name of the suspiciousness score to use for sorting
        """
        # If random, just sort by the sus scores
        if tiebreaker == "random":
            # Introduce some randomness before sorting
            random.shuffle(all_lines)
            all_lines.sort(
                key=lambda x: x.sus_scores[method],
                reverse=True,
            )
        # Otherwise, use the tiebreaker scores
        else:
            all_lines.sort(
                key=lambda x: (x.sus_scores[method], x.tiebreakers[tiebreaker]),
                reverse=True,
            )
        # store the sorted list as an attribute
        return all_lines

    @staticmethod # this may have to be ammended depending on ranges of formulas
    def calculate_severity(method: str, sus_score: float, rank: int, out_of: int):
        """Return a function to format strings according to score severity.

        Args:
            method (str): name of the suspiciousness method used
            sus_score (float): suspiciousness score of the line
            rank (int): the rank of this line in the sorted list
            out_of (int): length of the sorted list
        """
        # if sus_score <= 0:
        #     return PALETTE["safe"]

        if (
            method in ["tarantula", "ochiai", "ochiai2", "barinel", "jaccard", "kulczynski2"] # New formula
        ) and sus_score == 1:
            return PALETTE["severe"]

        if (
            method in ["tarantula", "ochiai", "ochiai2", "barinel", "jaccard", "kulczynski2, op2"] # New formula
        ) and sus_score == 0:
            return PALETTE["safe"]





        if (
            method in ["op2"] # New formula
        ) and sus_score > 1.3:
            return PALETTE["severe"]

        if (
            method in ["op2"] # New formula
        ) and sus_score < 1.3 and sus_score >= 1.0:
            return PALETTE["risky"]

        if (
            method in ["op2"] # New formula
        ) and sus_score >= 0.3 and sus_score < 1.0:
            return PALETTE["mild"]

        if (
            method in ["op2"] # New formula
        ) and sus_score < 0.3 and sus_score > 0:
            return PALETTE["safe"]





        if (
            method in ["mccon", "minus"] # New formula
        ) and sus_score == 1:
            return PALETTE["severe"]

        if (
            method in ["mccon", "minus"] # New formula
        ) and sus_score > 0 and sus_score < 1:
            return PALETTE["risky"]

        if (
            method in ["mccon", "minus"] # New formula
        ) and sus_score < 0 and sus_score > -1:
            return PALETTE["mild"]

        if (
            method in ["mccon", "minus"] # New formula
        ) and sus_score == -1:
            return PALETTE["safe"]





        if method == "dstar" and sus_score == float("inf"):
            return PALETTE["severe"]

        if method == "dstar" and sus_score <= 0:
            return PALETTE["safe"]

        



        if rank / out_of <= 0.2:
            return PALETTE["risky"]



        return PALETTE["mild"]
