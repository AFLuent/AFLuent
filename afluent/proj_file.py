"""Create object oriented structure for files carrying line coverage information."""
from afluent import line


class ProjFile:
    """Store coverage information about python files under test."""

    def __init__(self, name: str) -> None:
        """Initialize a ProjFile object.

        Args:
            name (str): name of the file under test
        """
        self.name = name
        self.lines = {}

    def add_line(self, line: line.Line):
        """Add a line to the self.lines based on the number of the line.add()

        Args:
            line (line.Line): Line object to add
        """
        self.lines[line.number] = line
