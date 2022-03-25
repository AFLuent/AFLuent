"""Define complexity generators and criteria to calculate complexity."""

from typing import Any, Dict, List, Tuple
import libcst as cst
from libcst import metadata
from libcst import matchers
import radon  # type: ignore[import]
import radon.complexity as cc  # type: ignore[import]

MUTANTS = [
    matchers.BitInvert,
    matchers.Not,
    matchers.Minus,
    matchers.Plus,
    matchers.And,
    matchers.Or,
    matchers.Add,
    matchers.BitAnd,
    matchers.BitOr,
    matchers.BitXor,
    matchers.Divide,
    matchers.FloorDivide,
    matchers.LeftShift,
    matchers.MatrixMultiply,
    matchers.Modulo,
    matchers.Multiply,
    matchers.Power,
    matchers.RightShift,
    matchers.Subtract,
    matchers.Equal,
    matchers.GreaterThan,
    matchers.GreaterThanEqual,
    matchers.In,
    matchers.Is,
    matchers.LessThan,
    matchers.LessThanEqual,
    matchers.NotEqual,
    matchers.IsNot,
    matchers.NotIn,
    matchers.AddAssign,
    matchers.BitAndAssign,
    matchers.BitOrAssign,
    matchers.BitXorAssign,
    matchers.DivideAssign,
    matchers.FloorDivideAssign,
    matchers.LeftShiftAssign,
    matchers.MatrixMultiplyAssign,
    matchers.ModuloAssign,
    matchers.MultiplyAssign,
    matchers.PowerAssign,
    matchers.RightShiftAssign,
    matchers.SubtractAssign,
]

ENHANCED_MUTANTS = [
    matchers.AnnAssign,
    matchers.Assign,
    matchers.Call,
    matchers.Subscript,
    matchers.Tuple,
    matchers.List,
    matchers.SimpleString,
    matchers.Dict,
    matchers.Integer,
    matchers.Float,
] + MUTANTS


class FullVisitor(cst.CSTVisitor):
    """Locate specific nodes and organize by line number and calculate their complexity."""

    METADATA_DEPENDENCIES = (metadata.PositionProvider,)

    def __init__(self, filler_dict: dict) -> None:
        """Initialize the class as a visitor.

        Args:
            filler_dict (dict): empty dictionary containing all line numbers of
            a file.
        """
        super().__init__()
        self.mutants_by_location = filler_dict
        self.score: Dict[int, float] = {}

    def visit_If(self, node: cst.If) -> None:
        """Store the metadata of if statements when visited."""
        node_metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(node_metadata)

    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        """Store the metadata of function definition when visited."""
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
        }
        return metadata_dict

    def fill_locations_range(self, node_metadata):
        """Distribute the metadata for all nodes in the same block."""
        start = node_metadata["start"]
        end = node_metadata["end"]
        for line_num in range(start, end + 1):
            if line_num in self.mutants_by_location:
                self.mutants_by_location[line_num].append(node_metadata)

    def calculate_score(self):
        """Iterate through the collected data and generate a score for each line."""
        for key, value in self.mutants_by_location.items():
            self.score[key] = FullVisitor.get_average_score(value)

    @staticmethod
    def get_average_score(items_list: List[Dict[str, Any]]) -> float:
        """Calculate the average score for a single line

        Args:
            items_list (List[Dict[str, Any]]): List of nodes with their
           information

        Returns:
            float: score for the line
        """
        statement_sum = 0
        statement_num = 0
        other_sum = 0
        other_num = 0
        # iterate through the list in a reverse order
        for item in items_list[::-1]:
            if item["type"] == "SimpleStatementLine":
                statement_sum += item["complexity"]
                statement_num += 1
            else:
                other_sum += item["complexity"]
                other_num += 1
        # avoid division by zero
        if statement_num == 0:
            statement_num += 1
        score = ((statement_sum / statement_num) + (other_sum / other_num)) / 2
        return round(score, 5)

    @staticmethod
    def count_mutants(node, mutant_set):
        """Count the number of possible mutants in a node using the MUTANTS variable."""
        total = 0
        for mutant in mutant_set:
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
        if node.test:
            total = FullVisitor.count_mutants(node.test, ENHANCED_MUTANTS)
            return total
        return 0

    @staticmethod
    def get_statement_complexity(node):
        """Calculate the complexity of a general statement."""
        # Complexity of a statement = number of mutants
        total = FullVisitor.count_mutants(node, ENHANCED_MUTANTS)
        return total

    @staticmethod
    def get_while_complexity(node):
        """Calculate the complexity of a while loop."""
        if node.test:
            total = FullVisitor.count_mutants(node.test, ENHANCED_MUTANTS)
            return total
        return 0

    @staticmethod
    def get_for_complexity(node):
        """Calculate the complexity of a for loop."""
        target_mutants = 0
        iterable_mutants = 0
        if node.target:
            target_mutants = FullVisitor.count_mutants(node.target, ENHANCED_MUTANTS)
        if node.iter:
            iterable_mutants = FullVisitor.count_mutants(node.iter, ENHANCED_MUTANTS)
        return target_mutants + iterable_mutants

    @staticmethod
    def get_with_complexity(node):
        """Calculate the complexity of a with statement."""
        if node.items:
            total = FullVisitor.count_mutants(node.items, ENHANCED_MUTANTS)
            return total
        return 0


COMPLEXITY_FUNC = {
    "FunctionDef": FullVisitor.get_funcdef_complexity,
    "If": FullVisitor.get_if_complexity,
    "SimpleStatementLine": FullVisitor.get_statement_complexity,
    "While": FullVisitor.get_while_complexity,
    "For": FullVisitor.get_for_complexity,
    "With": FullVisitor.get_with_complexity,
}


class StatementVisitor(cst.CSTVisitor):
    """Locate specific nodes and organize by line number and calculate their complexity."""

    METADATA_DEPENDENCIES = (metadata.PositionProvider,)

    def __init__(self, filler_dict: dict) -> None:
        """Initialize the class as a visitor.

        Args:
            filler_dict (dict): empty dictionary containing all line numbers of
            a file.
        """
        super().__init__()
        self.mutants_by_location = filler_dict

    def visit_SimpleStatementLine(self, node: cst.SimpleStatementLine) -> None:
        """Store the metadata of general statements when visited."""
        node_metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(node_metadata)

    def get_node_metadata_dict(self, node):
        """Organize the metadata dictionary."""
        node_type = type(node).__name__
        metadata_dict = {
            "start": self.get_metadata(metadata.PositionProvider, node).start.line,
            "end": self.get_metadata(metadata.PositionProvider, node).end.line,
            "type": node_type,
        }
        if node_type == "SimpleStatementLine":
            metadata_dict["complexity"] = StatementVisitor.get_statement_complexity(
                node
            )
        return metadata_dict

    def fill_locations_range(self, node_metadata):
        """Distribute the metadata for all nodes in the same block."""
        start = node_metadata["start"]
        end = node_metadata["end"]
        for line_num in range(start, end + 1):
            if line_num in self.mutants_by_location:
                self.mutants_by_location[line_num] = node_metadata["complexity"]

    @staticmethod
    def get_statement_complexity(node):
        """Calculate the complexity of a general statement."""
        # Complexity of a statement = number of mutants
        total = StatementVisitor.count_mutants(node)
        return total

    @staticmethod
    def count_mutants(node):
        """Count the number of possible mutants in a node using the MUTANTS variable."""
        total = 0
        for mutant in MUTANTS:
            total += len(matchers.findall(node, mutant()))
        return total


# pylint: disable=R0903
class EnhancedTieBreaker:
    """Store the full syntax mutant density data set and call the finder."""

    def __init__(self, file_path: str) -> None:
        """Initialize the generator."""
        self.path = file_path
        self.data: Dict[int, List[Dict[str, Any]]] = {}
        self.score: Dict[int, float] = {}

    def calculate_mutant_density(self):
        """Get the full file mutant density dataset."""
        with open(self.path, "r", encoding="utf-8") as infile:
            file_text = infile.read()
            module_obj = cst.parse_module(file_text)
        lines_num = len(file_text.splitlines())
        filler_dict = {i: [] for i in range(1, lines_num + 1)}
        wrapper = metadata.MetadataWrapper(module_obj)
        finder = FullVisitor(filler_dict)
        wrapper.visit(finder)
        self.data = finder.mutants_by_location
        finder.calculate_score()
        self.score = finder.score


# pylint: disable=R0903
class LogicalTieBreaker:
    """Store the full syntax mutant density data set and call the finder."""

    def __init__(self, file_path: str) -> None:
        """Initialize the generator."""
        self.path = file_path
        self.score: Dict[int, int] = {}

    def calculate_mutant_density(self):
        """Get the full file mutant density dataset."""
        with open(self.path, "r", encoding="utf-8") as infile:
            file_text = infile.read()
            module_obj = cst.parse_module(file_text)
        lines_num = len(file_text.splitlines())
        filler_dict = {i: 0 for i in range(1, lines_num + 1)}
        wrapper = metadata.MetadataWrapper(module_obj)
        finder = StatementVisitor(filler_dict)
        wrapper.visit(finder)
        self.score = finder.mutants_by_location


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
