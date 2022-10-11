"""Test the line module and Line class."""

import pytest

from afluent import line


def test_globals():
    """Check that global constants are of specific values."""
    assert line.TARAN == "tarantula"
    assert line.OCHIAI == "ochiai"
    assert line.OCHIAI2 == "ochiai2"
    assert line.DSTAR == "dstar"
    assert line.OP2 == "op2"  # New formula
    assert line.RANDOM == "random"
    assert line.CYCLOMATIC == "cyclomatic"
    assert line.LOGICAL == "logical"
    assert line.ENHANCED == "enhanced"


@pytest.mark.parametrize(
    "failed_cover,passed_cover,total_passed,total_failed,expected_score",
    [
        (1, 0, 1, 1, 1),
        (0, 1, 1, 1, 0),
        (3, 1, 6, 4, 0.8182),
        (0, 3, 5, 0, 0),
        (4, 0, 0, 9, 1),
    ],
)
def test_tarantula(
    failed_cover, passed_cover, total_passed, total_failed, expected_score
):
    """Check that the tarantula formula is correct."""
    assert (
        line.Line.tarantula(failed_cover, passed_cover, total_passed, total_failed)
        == expected_score
    )


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


@pytest.mark.parametrize(
    "failed_cover,passed_cover,total_failed,power,expected_score",
    [
        (1, 0, 2, 3, 1),
        (3, 2, 6, 3, 5.4),
        (0, 1, 6, 3, 0),
        (6, 0, 6, 3, float("inf")),
    ],
)
def test_dstar(failed_cover, passed_cover, total_failed, power, expected_score):
    """Check that the test_dstar formula is correct."""
    assert (
        line.Line.dstar(failed_cover, passed_cover, total_failed, power=power)
        == expected_score
    )


@pytest.mark.parametrize(
    "failed_cover,passed_cover,total_passed,total_failed,expected_score",
    [
        (3, 0, 0, 6, 1),
        (0, 0, 7, 0, 0),
        (3, 3, 3, 3, 0),
        (0, 0, 5, 5, 0),
        (3, 2, 7, 6, 0.366),
    ],
)
def test_ochiai2(
    failed_cover, passed_cover, total_passed, total_failed, expected_score
):
    """Check that the ochiai2 formula is correct."""
    assert (
        line.Line.ochiai2(failed_cover, passed_cover, total_passed, total_failed)
        == expected_score
    )


@pytest.mark.parametrize(
    "failed_cover,passed_cover,total_passed,expected_score",
    [
        (2, 2, 1, 1),
        (1, 1, 0, 0),
        (5, 2, 4, 4.6),
        (8, 6, 2, 6),
        (7, 0, 4, 7),
    ],
)
def test_op2(failed_cover, passed_cover, total_passed, expected_score):
    """Check that the op2 formula is correct."""
    assert line.Line.op2(failed_cover, passed_cover, total_passed) == expected_score


def test_line_create():
    """Check that line object can be instantiated correctly."""
    test_line = line.Line("sample/path/to/file.py", 14)
    assert test_line.path == "sample/path/to/file.py"
    assert test_line.number == 14
    assert not (test_line.passed_by or test_line.failed_by or test_line.skipped_by)
    assert list(test_line.sus_scores.values()) == [
        -1.0,
        -1.0,
        -1.0,
        -1.0,
        -1.0,
    ]  # New formula
    assert list(test_line.tiebreakers.values()) == [0, 0, 0, 0]


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
    with pytest.raises(Exception):
        test_line.sus("random", 5, 5)


def test_as_csv():
    """Check that a line is correctly converted to csv format."""
    test_line = line.Line("sample/path/to/file.py", 14)
    assert test_line.as_csv() == ["sample/path/to/file.py", 14, -1, -1, -1, -1, -1]


def test_sus_text():
    """Check that the correct tuple is returned."""
    test_line = line.Line("sample/path/to/file.py", 14)
    test_line.sus_scores = {
        "tarantula": 1.0,
        "ochiai": 1.0,
        "dstar": 15.0,
        "op2": 3.0,  # New formula
    }
    assert test_line.sus_text(["tarantula"]) == ("sample/path/to/file.py", 14, [1.0])
    assert test_line.sus_text(["ochiai"]) == ("sample/path/to/file.py", 14, [1.0])
    assert test_line.sus_text(["dstar"]) == ("sample/path/to/file.py", 14, [15.0])
    assert test_line.sus_text(["op2"]) == (
        "sample/path/to/file.py",
        14,
        [3.0],
    )  # New formula
    assert test_line.sus_text(["dstar", "tarantula"]) == (
        "sample/path/to/file.py",
        14,
        [15.0, 1.0],
    )


# def test_something():
#     """Purposefully fail to check report."""
#     assert False
