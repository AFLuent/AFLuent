"""Implement parsing and reassembling functions for coverage data."""


class Spectrum:
    """Store all the information for individual files and lines coverage."""

    def __init__(self, config) -> None:
        """Initialize a spectrum object.

        Args:
            config (dict): per-test coverage information
        """
        self.config = config
        self.reassembled_data = self.reassemble()

    def generate_report(self):
        """Generate and pretty print the AFL report."""
        print("here is the report")

    def reassemble(self):
        """Reassemble the coverage information on a file and line basis."""
        if not self.config:
            return {}

        for test_case_name, spectrum_dict in self.config.items():
            test_result = spectrum_dict["result"]
            for file_name, lines_covered in spectrum_dict["coverage"]:
                # TODO: implement this
                pass
