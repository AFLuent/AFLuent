"""Test the proj_file module and ProjFile class."""

from afluent import proj_file, line
import pytest


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
