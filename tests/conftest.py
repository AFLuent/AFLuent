"""Implement fixtures and hooks for pytest session."""

import json
import pathlib
import pytest

# pylint: disable=C0103,W0602
full_test_data = {}


@pytest.hookimpl()
def pytest_sessionstart():
    """Read and collect test data as part of the global test data dictionary."""
    test_data_files = pathlib.Path("./tests/test_data").glob("*.json")
    for json_data_file in test_data_files:
        with open(json_data_file, "r", encoding="utf-8") as data_file:
            current_test_data = json.load(data_file)
            global full_test_data
            full_test_data[json_data_file.stem] = current_test_data


@pytest.fixture
def test_data():
    """Return full_test_data."""
    return full_test_data
