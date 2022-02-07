"""Implement parsing and reassembling functions for coverage data."""


from afluent import proj_file
import json
from typing import Dict
from pprint import pprint


class Spectrum:
    """Store all the information for individual files and lines coverage."""

    def __init__(self, config) -> None:
        """Initialize a spectrum object.

        Args:
            config (dict): per-test coverage information
        """
        self.config = config
        self.reassembled_data: Dict[str, proj_file.ProjFile] = {}
        self.reassemble()

    def generate_report(self):
        """Generate and pretty print the AFL report."""
        print("here is the report")

    def reassemble(self):
        """Reassemble the coverage information on a file and line basis."""
        # Config is empty, return nothing
        if not self.config:
            return {}
        # iterate through every test case in the spectrum report
        for test_case_name, spectrum_dict in self.config.items():
            test_result = spectrum_dict["result"]
            for file_name, lines_covered in spectrum_dict["coverage"].items():
                if file_name not in self.reassembled_data:
                    self.reassembled_data[file_name] = proj_file.ProjFile(file_name)
                self.reassembled_data[file_name].update_file(
                    lines_covered, test_result, test_case_name
                )


if __name__ == "__main__":
    with open("../spectrum_data.json", "r") as infile:
        my_config = json.load(infile)

    my_spectrum = Spectrum(my_config)
    my_spectrum.reassemble()
    pprint(my_spectrum.reassembled_data)
