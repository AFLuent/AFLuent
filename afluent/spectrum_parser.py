"""Implement parsing and reassembling functions for coverage data."""

import json
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
        self.reassemble()

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
            for file_name, lines_covered in spectrum_dict["coverage"].items():
                if file_name not in self.reassembled_data:
                    self.reassembled_data[file_name] = proj_file.ProjFile(file_name)
                self.reassembled_data[file_name].update_file(
                    lines_covered, test_result, test_case_name
                )

    def as_dict(self):
        """Return the spectrum information as a JSON writable dictionary."""
        data_dict = {}
        for file_name, file_obj in self.reassembled_data.items():
            data_dict[file_name] = file_obj.as_dict()

        return data_dict


if __name__ == "__main__":
    with open("../spectrum_data.json", "r", encoding="utf-8") as infile:
        my_config = json.load(infile)

    my_spectrum = Spectrum(my_config)
    my_spectrum.reassemble()
    print(my_spectrum.as_dict())
