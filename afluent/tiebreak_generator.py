"""Define complexity generators and criteria to calculate complexity."""

from typing import Any, Dict, List, Tuple
import libcst as cst
from libcst import metadata
from libcst import matchers
import radon  # type: ignore[import]
import radon.complexity as cc  # type: ignore[import]

MUTANTS = [
    cst.BitInvert,
    cst.Not,
    cst.Minus,
    cst.Plus,
    cst.And,
    cst.Or,
    cst.Add,
    cst.BitAnd,
    cst.BitOr,
    cst.BitXor,
    cst.Divide,
    cst.FloorDivide,
    cst.LeftShift,
    cst.MatrixMultiply,
    cst.Modulo,
    cst.Multiply,
    cst.Power,
    cst.RightShift,
    cst.Subtract,
    cst.Equal,
    cst.GreaterThan,
    cst.GreaterThanEqual,
    cst.In,
    cst.Is,
    cst.LessThan,
    cst.LessThanEqual,
    cst.NotEqual,
    cst.IsNot,
    cst.NotIn,
    cst.AddAssign,
    cst.BitAndAssign,
    cst.BitOrAssign,
    cst.BitXorAssign,
    cst.DivideAssign,
    cst.FloorDivideAssign,
    cst.LeftShiftAssign,
    cst.MatrixMultiplyAssign,
    cst.ModuloAssign,
    cst.MultiplyAssign,
    cst.PowerAssign,
    cst.RightShiftAssign,
    cst.SubtractAssign,
]


class LocationFinder(cst.CSTVisitor):
    """Locate specific nodes and organize by line number and calculate their complexity."""

    METADATA_DEPENDENCIES = (metadata.PositionProvider,)

    def __init__(self, filler_dict: dict) -> None:
        """Initialize the class as a visitor.

        Args:
            filler_dict (dict): empty dictionary containing all line numbers of
            a file.
        """
        super().__init__()
        self.contents_by_location = filler_dict

    def visit_If(self, node: cst.If) -> None:
        """Store the metadata of if statements when visited."""
        node_metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(node_metadata)

    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        """Store the metadata of function definition when visited."""
        node_metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(node_metadata)

    def visit_Return(self, node: cst.Return) -> None:
        """Store the metadata of return statements when visited."""
        node_metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(node_metadata)

    def visit_SimpleStatementLine(self, node: cst.SimpleStatementLine) -> None:
        """Store the metadata of general statements when visited."""
        node_metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(node_metadata)

    def visit_While(self, node: cst.While) -> None:
        """Store the metadata of while loops when visited."""
        node_metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(node_metadata)

    def visit_For(self, node: cst.For) -> None:
        """Store the metadata of for loops when visited."""
        node_metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(node_metadata)

    def visit_With(self, node: cst.With) -> None:
        """Store the metadata of with statements when visited."""
        node_metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(node_metadata)

    def get_node_metadata_dict(self, node):
        """Organize the metadata dictionary."""
        node_type = type(node).__name__
        metadata_dict = {
            "start": self.get_metadata(metadata.PositionProvider, node).start.line,
            "end": self.get_metadata(metadata.PositionProvider, node).end.line,
            "type": node_type,
            "complexity": COMPLEXITY_FUNC[node_type](node),
            # TODO: remove this
            # "node": node,
        }
        return metadata_dict

    def fill_locations_range(self, node_metadata):
        """Distribute the metadata for all nodes in the same block."""
        start = node_metadata["start"]
        end = node_metadata["end"]
        for line_num in range(start, end + 1):
            if line_num in self.contents_by_location:
                self.contents_by_location[line_num].append(node_metadata)

    # complexity calculation:
    # number of mutant density in statement
    # number of arguments in a function

    # Define complexity for:
    # FunctionDef: simply call match the number of parameters in node.params
    # If: check node.test, check if node.orelse exists and parse that too
    # SimpleStatementLine: match all its children
    # Return: match node.value
    # While: check node.test
    # For: not clear, there is target and iter to check but they're relatively low complexity
    # With: check node.items

    @staticmethod
    def count_mutants(node):
        """Count the number of possible mutants in a node using the MUTANTS variable."""
        total = 0
        for mutant in MUTANTS:
            total += len(matchers.findall(node, mutant()))
        return total

    @staticmethod
    def get_funcdef_complexity(node):
        """Calculate the complexity of a function definition."""
        return len(node.params.params)

    @staticmethod
    def get_if_complexity(node):
        """Calculate the complexity of an if statement."""
        # complexity of if statement= number of mutants in the test condition
        total = LocationFinder.count_mutants(node.test)
        return total

    @staticmethod
    def get_statement_complexity(node):
        """Calculate the complexity of a general statement."""
        # Complexity of a statement = number of mutants
        total = LocationFinder.count_mutants(node)
        return total

    @staticmethod
    def get_return_complexity(node):
        """Calculate the complexity of a return statement."""
        total = LocationFinder.count_mutants(node.value)
        return total

    @staticmethod
    def get_while_complexity(node):
        """Calculate the complexity of a while loop."""
        total = LocationFinder.count_mutants(node.test)
        return total

    @staticmethod
    def get_for_complexity(node):
        """Calculate the complexity of a for loop."""
        # TODO: implement me
        return 0

    @staticmethod
    def get_with_complexity(node):
        """Calculate the complexity of a with statement."""
        total = LocationFinder.count_mutants(node.items)
        return total


COMPLEXITY_FUNC = {
    "FunctionDef": LocationFinder.get_funcdef_complexity,
    "If": LocationFinder.get_if_complexity,
    "SimpleStatementLine": LocationFinder.get_statement_complexity,
    "Return": LocationFinder.get_return_complexity,
    "While": LocationFinder.get_while_complexity,
    "For": LocationFinder.get_for_complexity,
    "With": LocationFinder.get_with_complexity,
}


# pylint: disable=R0903
class SyntaxComplexityGenerator:
    """Store the full syntax complexity data set and call the finder."""

    def __init__(self, file_path: str) -> None:
        """Initialize the generator."""
        self.path = file_path
        self.data: Dict[int, List[Dict[str, Any]]] = {}

    def calculate_syntax_complexity(self):
        """Get the full file complexity dataset."""
        with open(self.path, "r", encoding="utf-8") as infile:
            file_text = infile.read()
            module_obj = cst.parse_module(file_text)
        lines_num = len(file_text.splitlines())
        filler_dict = {i: [] for i in range(1, lines_num + 1)}
        wrapper = metadata.MetadataWrapper(module_obj)
        finder = LocationFinder(filler_dict)
        wrapper.visit(finder)
        self.data = finder.contents_by_location


# pylint: disable=R0903
class CyclomaticComplexityGenerator:
    """Store the dataset for cyclomatic complexity in the file."""

    def __init__(self, file_path) -> None:
        """Initialize the generator."""
        self.path = file_path
        self.data: Dict[int, int] = {}

    def calculate_syntax_complexity(self):
        """Get the full dataset for cyclomatic complexity."""
        with open(self.path, "r", encoding="utf-8") as infile:
            file_string = infile.read()
            lines_num = len(file_string.splitlines())
            complexity_data = cc.sorted_results(cc.cc_visit(file_string), cc.LINES)
        filler_dict = {i: 0 for i in range(1, lines_num + 1)}
        # reassemble complexity data to follow this format
        # List(Tuple(line_start:int, line_end:int, complexity_score:int))
        for item in complexity_data:
            # Check if the current item is a Function and add it's information
            if isinstance(item, radon.visitors.Function):
                # fill the filler_dict with the complexity score
                for number in range(item.lineno, item.endline + 1):
                    filler_dict[number] = item.complexity
        self.data = filler_dict
