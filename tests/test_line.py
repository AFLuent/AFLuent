"""Test the line module and Line class."""

import pytest

from afluent import line


# TODO: add more input and expected output
@pytest.mark.parametrize(
    "failed_cover,passed_cover,total_passed,total_failed,expected_score",
    [(1, 0, 1, 1, 1), (0, 1, 1, 1, 0), (3, 1, 6, 4, 0.8182)],
)
def test_tarantula(
    failed_cover, passed_cover, total_passed, total_failed, expected_score
):
    """Check that the tarantula formula is correct."""
    assert (
        line.Line.tarantula(failed_cover, passed_cover, total_passed, total_failed)
        == expected_score
    )


# TODO: add more input and expected output
@pytest.mark.parametrize(
    "failed_cover,passed_cover,total_failed,expected_score",
    [
        (1, 0, 1, 1),
        (3, 2, 6, 0.5477),
        (0, 1, 6, 0),
    ],
)
def test_ohiai(failed_cover, passed_cover, total_failed, expected_score):
    """Check that the ohiai formula is correct."""
    assert line.Line.ochiai(failed_cover, passed_cover, total_failed) == expected_score


# TODO: add more input and expected output
@pytest.mark.parametrize(
    "failed_cover,passed_cover,total_failed,power,expected_score",
    [
        (1, 0, 2, 3, 1),
        (3, 2, 6, 3, 5.4),
        (0, 1, 6, 3, 0),
    ],
)
def test_dstar(failed_cover, passed_cover, total_failed, power, expected_score):
    """Check that the test_dstar formula is correct."""
    assert (
        line.Line.dstar(failed_cover, passed_cover, total_failed, power=power)
        == expected_score
    )


def test_line_create():
    """Check that line object can be instantiated correctly."""
    test_line = line.Line("sample/path/to/file.py", 14)
    assert test_line.path == "sample/path/to/file.py"
    assert test_line.number == 14
    assert not (test_line.passed_by or test_line.failed_by or test_line.skipped_by)


def test_line_sus_all():
    """Check that all suspiciousness scores can be calculated."""
    test_line = line.Line("sample/path/to/file.py", 14)
    test_line.passed_by = ["test1", "test2"]
    test_line.failed_by = ["test3", "test4", "test5"]
    for sus_value in test_line.sus_scores.values():
        assert sus_value == -1.0
    test_line.sus_all(4, 6)
    assert test_line.sus_scores["tarantula"] == 0.5
    assert test_line.sus_scores["ochiai"] == 0.5477
    assert test_line.sus_scores["dstar"] == 5.4


def test_line_sus_unknown():
    """Check that an error is thrown when an unknown method is passed."""
    test_line = line.Line("sample/path/to/file.py", 14)
    test_line.passed_by = ["test1", "test2"]
    test_line.failed_by = ["test3", "test4", "test5"]
    test_line.failed_total = 6
    test_line.passed_total = 4
    with pytest.raises(Exception):
        test_line.sus("random", 5, 5)


def test_line_as_dict():
    """Check that as_dict() return a correct dictionary."""
    test_line = line.Line("sample/path/to/file.py", 14)
    test_line.passed_by = ["test1", "test2"]
    test_line.failed_by = ["test3", "test4", "test5"]
    output_dict = test_line.as_dict()
    expected_dict = {
        "path": "sample/path/to/file.py",
        "number": 14,
        "passed_by": ["test1", "test2"],
        "failed_by": ["test3", "test4", "test5"],
        "skipped_by": [],
        "sus_scores": {
            "tarantula": -1.0,
            "ochiai": -1.0,
            "dstar": -1.0,
        },
        "complexity": 0,
    }
    assert output_dict == expected_dict


def test_sus_text():
    """Check that the correct tuple is returned."""
    test_line = line.Line("sample/path/to/file.py", 14)
    test_line.sus_scores = {
        "tarantula": 1.0,
        "ochiai": 1.0,
        "dstar": 15.0,
    }
    assert test_line.sus_text(["tarantula"]) == ("sample/path/to/file.py", 14, [1.0])
    assert test_line.sus_text(["ochiai"]) == ("sample/path/to/file.py", 14, [1.0])
    assert test_line.sus_text(["dstar"]) == ("sample/path/to/file.py", 14, [15.0])
    assert test_line.sus_text(["dstar", "tarantula"]) == (
        "sample/path/to/file.py",
        14,
        [15.0, 1.0],
    )


# def test_something():
#     """Purposefully fail to check report."""
#     # TODO: remove me
#     assert False
