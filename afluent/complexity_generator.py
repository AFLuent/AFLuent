import libcst as cst
import libcst.metadata as metdata
from typing import Any, Dict, List, Tuple


# Define visits for:
# If
# Else
# FunctionDef
# SimpleStatementLine
# Return
# While
# For
# With


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

    def visit_Else(self, node: cst.FunctionDef) -> None:
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
        # TODO: can we recursively construct this using self.visit?
        node_type = type(node).__name__
        metadata_dict = {
            "start": self.get_metadata(metdata.PositionProvider, node).start.line,
            "end": self.get_metadata(metdata.PositionProvider, node).end.line,
            "type": node_type,
            "complexity": LocationFinder.get_complexity(node, node_type),
            # TODO: uncomment this
            # "node": node,
        }
        if not (node_type == "SimpleStatementLine" or node_type == "Return"):
            metadata_dict["contents"] = []
        return metadata_dict

    def fill_locations_range(self, metadata):
        start = metadata["start"]
        end = metadata["end"]
        for line_num in range(start, end + 1):
            if line_num in self.contents_by_location:
                self.contents_by_location[line_num].append(metadata)

    @staticmethod
    def get_complexity(node, node_type):
        # TODO: implement
        return 0


class SyntaxtComplexityGenerator:
    def __init__(self, file_path: str) -> None:
        self.path = file_path
        self.contents_by_location: Dict[int, List[Dict[str, Any]]] = {}

    def calculate_syntax_complexity(self):
        with open(self.path, "r", encoding="utf-8") as infile:
            file_text = infile.read()
            module_obj = cst.parse_module(file_text)
        lines_num = len(file_text.splitlines())
        filler_dict = {i: [] for i in range(1, lines_num + 1)}
        wrapper = metdata.MetadataWrapper(module_obj)
        finder = LocationFinder(filler_dict)
        wrapper.visit(finder)
        self.contents_by_location = finder.contents_by_location
