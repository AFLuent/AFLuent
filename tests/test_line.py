"""Test the line module and Line class."""

import pytest

from afluent import line


def test_globals():   # New Formula
    """Check that global constants are of specific values."""
    assert line.TARAN == "tarantula"
    assert line.OCHIAI == "ochiai"
    assert line.OCHIAI2 == "ochiai2"
    assert line.DSTAR == "dstar"
    assert line.OP2 == "op2"
    assert line.BARINEL == "barinel"
    assert line.JACCARD == "jaccard"
    assert line.KULCZYNSKI == "kulczynski"
    assert line.KULCZYNSKI2 == "kulczynski2"
    assert line.MCCON == "mccon"
    assert line.MINUS == "minus"
    assert line.ZOLTAR == "zoltar"
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
    "failed_cover,passed_cover,total_passed,total_failed,expected_score",
    [
        (9, 13, 19, 28, 0.4091),
        (17, 3, 26, 34, 0.8500),
        (1, 23, 25, 9, 0.0417),
        (0, 11, 32, 24, 0.0000),
        (6, 6, 19, 22, 0.5000),
        (3, 7, 23, 26, 0.3000),
        (8, 10, 12, 14, 0.4444),
        (20, 2, 15, 40, 0.9091),
        (20, 14, 30, 26, 0.5882),
        (18, 4, 8, 28, 0.8182),
        (6, 7, 20, 12, 0.4615),
        (23, 10, 29, 44, 0.6970),
        (20, 16, 23, 38, 0.5556),
        (16, 10, 27, 21, 0.6154),
        (10, 20, 22, 31, 0.3333),
        (0, 2, 9, 6, 0.0000),
        (19, 23, 37, 21, 0.4524),
        (16, 9, 20, 18, 0.6400),
        (5, 16, 39, 9, 0.2381),
        (9, 13, 35, 15, 0.4091),
        (14, 12, 13, 26, 0.5385),
        (24, 13, 33, 35, 0.6486),
        (2, 20, 22, 13, 0.0909),
        (20, 18, 18, 37, 0.5263),
        (13, 19, 21, 16, 0.4062),
        (8, 13, 13, 11, 0.3810),
    ],
)
def test_barinel(
    failed_cover, passed_cover, total_passed, total_failed, expected_score
):
    """Check that the Barinel formula is correct."""
    assert (
        line.Line.barinel(failed_cover, passed_cover, total_passed, total_failed)
        == expected_score
    )







@pytest.mark.parametrize(
    "failed_cover,passed_cover,total_passed,total_failed,expected_score",
    [
        (5, 21, 43, 15, 0.1389),
        (4, 21, 30, 27, 0.0833),
        (15, 11, 11, 28, 0.3846),
        (13, 21, 33, 22, 0.3023),
        (22, 24, 29, 44, 0.3235),
        (19, 17, 39, 28, 0.4222),
        (4, 13, 20, 12, 0.1600),
        (14, 18, 30, 20, 0.3684),
        (9, 3, 11, 14, 0.5294),
        (23, 23, 46, 41, 0.3594),
        (11, 10, 23, 15, 0.4400),
        (13, 22, 26, 27, 0.2653),
        (14, 21, 31, 15, 0.3889),
        (19, 20, 28, 31, 0.3725),
        (17, 17, 35, 32, 0.3469),
        (21, 14, 38, 31, 0.4667),
        (16, 20, 22, 26, 0.3478),
        (24, 5, 6, 34, 0.6154),
        (20, 6, 24, 31, 0.5405),
        (11, 7, 28, 14, 0.5238),
        (14, 10, 31, 19, 0.4828),
        (18, 11, 29, 20, 0.5806),
        (3, 15, 28, 23, 0.0789),
        (5, 4, 20, 11, 0.3333),
        (19, 24, 37, 27, 0.3725),
        (23, 1, 5, 39, 0.5750),
    ],
)
def test_jaccard(
    failed_cover, passed_cover, total_passed, total_failed, expected_score
):
    """Check that the Jaccard formula is correct."""
    assert (
        line.Line.jaccard(failed_cover, passed_cover, total_passed, total_failed)
        == expected_score
    )







@pytest.mark.parametrize(
    "failed_cover,passed_cover,total_passed,total_failed,expected_score",
    [
        (8, 6, 20, 14, 0.6667),
        (18, 13, 33, 38, 0.5455),
        (1, 11, 28, 12, 0.0455),
        (11, 4, 14, 27, 0.5500),
        (1, 17, 31, 8, 0.0417),
        (11, 2, 7, 15, 1.8333),
        (0, 23, 44, 11, 0.0000),
        (14, 6, 14, 16, 1.7500),
        (19, 12, 30, 38, 0.6129),
        (22, 0, 16, 45, 0.9565),
        (3, 7, 27, 12, 0.1875),
        (8, 15, 20, 12, 0.4211),
        (11, 5, 23, 17, 1.0000),
        (21, 11, 14, 31, 1.0000),
        (2, 2, 3, 22, 0.0909),
        (23, 16, 28, 44, 0.6216),
        (0, 14, 22, 4, 0.0000),
        (18, 18, 34, 26, 0.6923),
        (4, 11, 17, 27, 0.1176),
        (9, 16, 17, 20, 0.3333),
        (17, 11, 14, 29, 0.7391),
        (18, 21, 23, 19, 0.8182),
        (21, 18, 25, 33, 0.7000),
        (0, 17, 17, 23, 0.0000),
        (17, 0, 21, 27, 1.7000),
        (20, 6, 24, 26, 1.6667),
    ],
)
def test_kulczynski(
    failed_cover, passed_cover, total_passed, total_failed, expected_score
):
    """Check that the Kulczynski formula is correct."""
    assert (
        line.Line.kulczynski(failed_cover, passed_cover, total_passed, total_failed)
        == expected_score
    )






@pytest.mark.parametrize(
    "failed_cover,passed_cover,total_passed,total_failed,expected_score",
    [
        (24, 3, 22, 26, 0.9060),
        (2, 12, 20, 19, 0.1241),
        (17, 13, 37, 22, 0.6697),
        (19, 22, 40, 22, 0.6635),
        (23, 18, 37, 29, 0.6770),
        (24, 22, 38, 34, 0.6138),
        (23, 15, 23, 42, 0.5764),
        (12, 18, 22, 19, 0.5158),
        (14, 12, 16, 24, 0.5609),
        (8, 4, 25, 11, 0.6970),
        (12, 24, 37, 24, 0.4167),
        (5, 5, 14, 8, 0.5625),
        (0, 2, 25, 1, 0.0000),
        (8, 14, 25, 10, 0.5818),
        (11, 1, 25, 30, 0.6417),
        (15, 8, 19, 26, 0.6145),
        (9, 15, 25, 12, 0.5625),
        (20, 14, 26, 36, 0.5719),
        (9, 24, 38, 20, 0.3614),
        (4, 15, 27, 6, 0.4386),
        (23, 19, 38, 46, 0.5238),
        (13, 18, 26, 37, 0.3854),
        (9, 1, 23, 32, 0.5906),
        (14, 10, 10, 38, 0.4759),
        (18, 17, 41, 28, 0.5786),
        (6, 10, 30, 11, 0.4602),
    ],
)
def test_kulczynski2(
    failed_cover, passed_cover, total_passed, total_failed, expected_score
):
    """Check that the Kulczynski2 formula is correct."""
    assert (
        line.Line.kulczynski2(failed_cover, passed_cover, total_passed, total_failed)
        == expected_score
    )







@pytest.mark.parametrize(
    "failed_cover,passed_cover,total_passed,total_failed,expected_score",
    [
        (11, 8, 8, 28, -0.0282),
        (4, 18, 20, 14, -0.5325),
        (20, 5, 24, 44, 0.2545),
        (9, 11, 31, 32, -0.2687),
        (11, 5, 8, 20, 0.2375),
        (20, 7, 22, 27, 0.4815),
        (15, 21, 41, 30, -0.0833),
        (4, 19, 33, 10, -0.4261),
        (5, 23, 47, 11, -0.3669),
        (6, 1, 6, 16, 0.2321),
        (15, 11, 19, 15, 0.5769),
        (3, 21, 41, 19, -0.7171),
        (2, 17, 17, 10, -0.6947),
        (24, 17, 27, 29, 0.4130),
        (6, 0, 10, 9, 0.6667),
        (2, 14, 35, 14, -0.7321),
        (11, 4, 27, 17, 0.3804),
        (22, 16, 20, 29, 0.3376),
        (16, 2, 12, 35, 0.3460),
        (10, 18, 42, 22, -0.1883),
        (4, 2, 21, 6, 0.3333),
        (11, 23, 36, 34, -0.3529),
        (7, 1, 7, 19, 0.2434),
        (20, 22, 27, 40, -0.0238),
        (5, 9, 33, 22, -0.4156),
        (14, 8, 21, 22, 0.2727),
    ],
)
def test_mccon(
    failed_cover, passed_cover, total_passed, total_failed, expected_score
):
    """Check that the McCon formula is correct."""
    assert (
        line.Line.mccon(failed_cover, passed_cover, total_passed, total_failed)
        == expected_score
    )






@pytest.mark.parametrize(
    "failed_cover,passed_cover,total_passed,total_failed,expected_score",
    [
        (7, 11, 17, 25, -0.3690),
        (18, 13, 16, 30, -0.2561),
        (3, 21, 33, 10, -0.3377),
        (6, 2, 3, 18, -0.3333),
        (16, 3, 12, 17, 0.7174),
        (5, 0, 23, 24, 0.5581),
        (13, 4, 21, 20, 0.4715),
        (17, 9, 16, 41, -0.1479),
        (19, 22, 24, 22, -0.1356),
        (1, 4, 5, 7, -0.6593),
        (9, 10, 27, 29, -0.0668),
        (1, 2, 12, 3, 0.2222),
        (14, 8, 31, 26, 0.2925),
        (21, 3, 26, 44, 0.4339),
        (21, 9, 21, 40, 0.0966),
        (11, 24, 29, 24, -0.4021),
        (23, 23, 24, 23, 0.5106),
        (14, 8, 15, 27, -0.0149),
        (1, 5, 13, 6, -0.2729),
        (8, 15, 27, 20, -0.1559),
        (17, 24, 47, 39, -0.0750),
        (5, 9, 9, 7, -0.5833),
        (3, 21, 44, 20, -0.3801),
        (10, 6, 15, 32, -0.0954),
        (12, 5, 23, 36, 0.1453),
        (21, 8, 17, 33, 0.1677),
    ],
)
def test_minus(
    failed_cover, passed_cover, total_passed, total_failed, expected_score
):
    """Check that the Minus formula is correct."""
    assert (
        line.Line.minus(failed_cover, passed_cover, total_passed, total_failed)
        == expected_score
    )






@pytest.mark.parametrize(
    "failed_cover,passed_cover,total_passed,total_failed,expected_score",
    [
        (12, 20, 40, 29, 0.0000),
        (24, 2, 7, 27, 0.0095),
        (14, 12, 16, 23, 0.0002),
        (14, 2, 5, 26, 0.0008),
        (9, 2, 7, 22, 0.0003),
        (1, 7, 30, 14, 0.0000),
        (12, 23, 47, 12, 0.3429),
        (12, 14, 19, 24, 0.0001),
        (8, 4, 26, 29, 0.0001),
        (9, 7, 16, 10, 0.0012),
        (11, 1, 6, 21, 0.0012),
        (16, 7, 20, 38, 0.0002),
        (17, 4, 24, 37, 0.0004),
        (20, 17, 32, 44, 0.0001),
        (12, 23, 36, 15, 0.0002),
        (3, 20, 20, 7, 0.0000),
        (18, 1, 20, 20, 0.0159),
        (24, 15, 19, 32, 0.0005),
        (13, 3, 5, 14, 0.0056),
        (20, 11, 14, 33, 0.0003),
        (20, 10, 22, 28, 0.0005),
        (4, 17, 27, 17, 0.0000),
        (18, 23, 46, 30, 0.0001),
        (3, 22, 22, 6, 0.0000),
        (8, 1, 13, 11, 0.0021),
        (5, 14, 26, 17, 0.0000),
    ],
)
def test_zoltar(
    failed_cover, passed_cover, total_passed, total_failed, expected_score
):
    """Check that the Zoltar formula is correct."""
    assert (
        line.Line.zoltar(failed_cover, passed_cover, total_passed, total_failed)
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
        -1,
        -1,
        -1,
        -1,
        -1,
        -1,
        -1,
        -1,
        -1,
        -1,
        -1,
        -1,
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
    assert test_line.as_csv() == ["sample/path/to/file.py", 14, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]


def test_sus_text():
    """Check that the correct tuple is returned."""
    test_line = line.Line("sample/path/to/file.py", 14)
    test_line.sus_scores = {
        "tarantula": 1,
        "ochiai": 1,
        "dstar": 15,
        "op2": 3,  # New formula
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
        [15, 1.0],
    )


# def test_something():
#     """Purposefully fail to check report."""
#     assert False
