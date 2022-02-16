"""Test the proj_file module and ProjFile class."""

import pytest
from afluent import line, proj_file


def test_projfile_init():
    """Test that a projFile object can be created."""
    test_projfile = proj_file.ProjFile("samplename.py")
    assert test_projfile.name == "samplename.py"
    assert not test_projfile.lines


def test_update_file_new_key():
    """Check that a line is created and updated in a new file."""
    test_projfile = proj_file.ProjFile("samplename.py")
    covered_lines = [3, 6, 7, 9, 13]
    test_projfile.update_file(covered_lines, "passed", "sample_testcase")
    for line_num in covered_lines:
        assert line_num in test_projfile.lines
        assert isinstance(test_projfile.lines[line_num], line.Line)
        assert test_projfile.lines[line_num].passed_by == ["sample_testcase"]


def test_update_file_existing_key_passed():
    """Check that a line is created and updated in a new file."""
    test_projfile = proj_file.ProjFile("samplename.py")
    test_projfile.lines[5] = line.Line("samplename.py", 5)
    test_projfile.lines[5].passed_by = [
        "sample_testcase2",
        "sample_testcase3",
        "sample_testcase4",
    ]
    covered_lines = [5, 6]
    test_projfile.update_file(covered_lines, "passed", "sample_testcase")
    assert test_projfile.lines[5].passed_by == [
        "sample_testcase2",
        "sample_testcase3",
        "sample_testcase4",
        "sample_testcase",
    ]


def test_update_file_existing_key_failed():
    """Check that a line is created and updated in a new file."""
    test_projfile = proj_file.ProjFile("samplename.py")
    test_projfile.lines[5] = line.Line("samplename.py", 5)
    test_projfile.lines[5].failed_by = [
        "sample_testcase2",
        "sample_testcase3",
        "sample_testcase4",
    ]
    covered_lines = [5, 6]
    test_projfile.update_file(covered_lines, "failed", "sample_testcase")
    assert test_projfile.lines[5].failed_by == [
        "sample_testcase2",
        "sample_testcase3",
        "sample_testcase4",
        "sample_testcase",
    ]


def test_update_file_existing_key_skipped():
    """Check that a line is created and updated in a new file."""
    test_projfile = proj_file.ProjFile("samplename.py")
    test_projfile.lines[5] = line.Line("samplename.py", 5)
    test_projfile.lines[5].skipped_by = [
        "sample_testcase2",
        "sample_testcase3",
        "sample_testcase4",
    ]
    covered_lines = [5, 6]
    test_projfile.update_file(covered_lines, "skipped", "sample_testcase")
    assert test_projfile.lines[5].skipped_by == [
        "sample_testcase2",
        "sample_testcase3",
        "sample_testcase4",
        "sample_testcase",
    ]


def test_update_file_unknown_result():
    """Check that a line is created and updated in a new file."""
    test_projfile = proj_file.ProjFile("samplename.py")
    covered_lines = [5, 6]
    with pytest.raises(Exception):
        test_projfile.update_file(covered_lines, "random", "sample_testcase")


def test_projfile_as_dict():
    """Check that as_dict() return a correct dictionary."""
    file_name = "samplename.py"
    test_projfile = proj_file.ProjFile(file_name)
    test_projfile.update_file([5], "passed", "sample_test")
    output_dict = test_projfile.as_dict()
    expected_line = line.Line(file_name, 5)
    expected_line.passed_by = ["sample_test"]
    expected_dict = {"5": expected_line.as_dict()}
    assert output_dict == expected_dict
