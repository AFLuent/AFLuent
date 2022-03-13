import libcst as cst
import libcst.metadata as metdata
from typing import Any, Dict, List, Tuple
import radon  # type: ignore[import]
import radon.complexity as cc  # type: ignore[import]


class LocationFinder(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (metdata.PositionProvider,)

    def __init__(self, filler_dict) -> None:
        super().__init__()
        self.contents_by_location = filler_dict

    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(metadata)

    def visit_If(self, node: cst.FunctionDef) -> None:
        metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(metadata)

    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(metadata)

    def visit_Return(self, node: cst.FunctionDef) -> None:
        metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(metadata)

    def visit_SimpleStatementLine(self, node: cst.FunctionDef) -> None:
        metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(metadata)

    def visit_While(self, node: cst.FunctionDef) -> None:
        metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(metadata)

    def visit_For(self, node: cst.FunctionDef) -> None:
        metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(metadata)

    def visit_With(self, node: cst.FunctionDef) -> None:
        metadata = self.get_node_metadata_dict(node)
        self.fill_locations_range(metadata)

    def get_node_metadata_dict(self, node):
        node_type = type(node).__name__
        metadata_dict = {
            "start": self.get_metadata(metdata.PositionProvider, node).start.line,
            "end": self.get_metadata(metdata.PositionProvider, node).end.line,
            "type": node_type,
            "complexity": COMPLEXITY_FUNC[node_type](node),
            # TODO: remove this
            # "node": node,
        }
        return metadata_dict

    def fill_locations_range(self, metadata):
        start = metadata["start"]
        end = metadata["end"]
        for line_num in range(start, end + 1):
            if line_num in self.contents_by_location:
                self.contents_by_location[line_num].append(metadata)

    @staticmethod
    def get_funcdef_complexity(node):
        # TODO: implement me
        return 0

    @staticmethod
    def get_if_complexity(node):
        # TODO: implement me
        return 0

    @staticmethod
    def get_statement_complexity(node):
        # TODO: implement me
        return 0

    @staticmethod
    def get_return_complexity(node):
        # TODO: implement me
        return 0

    @staticmethod
    def get_while_complexity(node):
        # TODO: implement me
        return 0

    @staticmethod
    def get_for_complexity(node):
        # TODO: implement me
        return 0

    @staticmethod
    def get_with_complexity(node):
        # TODO: implement me
        return 0


COMPLEXITY_FUNC = {
    "FunctionDef": LocationFinder.get_funcdef_complexity,
    "If": LocationFinder.get_if_complexity,
    "SimpleStatementLine": LocationFinder.get_statement_complexity,
    "Return": LocationFinder.get_return_complexity,
    "While": LocationFinder.get_while_complexity,
    "For": LocationFinder.get_for_complexity,
    "With": LocationFinder.get_with_complexity,
}
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


class SyntaxtComplexityGenerator:
    def __init__(self, file_path: str) -> None:
        self.path = file_path
        self.data: Dict[int, List[Dict[str, Any]]] = {}

    def calculate_syntax_complexity(self):
        with open(self.path, "r", encoding="utf-8") as infile:
            file_text = infile.read()
            module_obj = cst.parse_module(file_text)
        lines_num = len(file_text.splitlines())
        filler_dict = {i: [] for i in range(1, lines_num + 1)}
        wrapper = metdata.MetadataWrapper(module_obj)
        finder = LocationFinder(filler_dict)
        wrapper.visit(finder)
        self.data = finder.contents_by_location


class CyclomaticComplexityGenerator:
    def __init__(self, file_path) -> None:
        self.path = file_path
        self.data: List[Tuple[int, int, int]] = []

    def calculate_syntax_complexity(self):
        with open(self.path, "r", encoding="utf-8") as infile:
            file_string = infile.read()
            complexity_data = cc.sorted_results(cc.cc_visit(file_string), cc.LINES)
        # reassemble complexity data to follow this format
        # List(Tuple(line_start:int, line_end:int, complexity_score:int))
        cc_lines = []
        for item in complexity_data:
            # Check if the current item is a Function and add it's information
            if isinstance(item, radon.visitors.Function):
                cc_lines.append((item.lineno, item.endline, item.complexity))
        self.data = cc_lines


# TODO: implement complexity by line where the raw data is processed
