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
        (20, 10, 6, 12, 0.6667),
        (1, 11, 12, 7, 0.0833),
        (18, 14, 10, 12, 0.5625),
        (10, 3, 10, 12, 0.7692),
        (12, 1, 9, 20, 0.9231),
        (15, 3, 13, 11, 0.8333),
        (5, 8, 9, 4, 0.3846),
        (3, 11, 14, 19, 0.2143),
        (9, 10, 4, 4, 0.4737),
        (14, 19, 17, 10, 0.4242),
        (18, 10, 17, 15, 0.6429),
        (20, 8, 7, 18, 0.7143),
        (20, 19, 3, 16, 0.5128),
        (20, 8, 14, 12, 0.7143),
        (3, 5, 19, 1, 0.3750),
        (0, 18, 1, 18, 0.0000),
        (20, 16, 12, 0, 0.5556),
        (7, 20, 20, 12, 0.2593),
        (16, 14, 16, 14, 0.5333),
        (3, 7, 11, 11, 0.3000),
        (2, 0, 14, 19, 1.0000),
        (4, 5, 14, 0, 0.4444),
        (20, 14, 18, 0, 0.5882),
        (17, 3, 12, 1, 0.8500),
        (18, 2, 14, 17, 0.9000),
        (20, 1, 3, 5, 0.9524),
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
        (19, 1, 2, 5, 3.1667),
        (2, 12, 9, 11, 0.0870),
        (13, 15, 18, 6, 0.6190),
        (15, 14, 10, 9, 0.6522),
        (12, 11, 0, 15, 0.4615),
        (17, 1, 10, 16, 1.0000),
        (20, 5, 11, 8, 1.5385),
        (2, 17, 2, 10, 0.0741),
        (6, 4, 19, 2, 1.0000),
        (13, 16, 8, 2, 0.7222),
        (4, 14, 1, 5, 0.2105),
        (11, 0, 20, 19, 0.5789),
        (14, 7, 13, 17, 0.5833),
        (4, 18, 11, 3, 0.1905),
        (6, 8, 0, 9, 0.3529),
        (17, 1, 3, 6, 2.4286),
        (9, 18, 19, 13, 0.2903),
        (11, 6, 5, 7, 0.8462),
        (7, 1, 19, 6, 1.0000),
        (17, 19, 5, 19, 0.4474),
        (12, 18, 16, 3, 0.5714),
        (8, 20, 11, 10, 0.2667),
        (19, 9, 15, 17, 0.7308),
        (9, 0, 16, 17, 0.5294),
        (8, 3, 5, 1, 2.0000),
        (5, 8, 9, 15, 0.2174),
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
        (5, 9, 14, 5, 0.5556),
        (20, 16, 5, 0, -5.0000),
        (6, 2, 1, 5, 6.0000),
        (12, 16, 15, 18, 0.5455),
        (20, 7, 11, 10, -6.6667),
        (18, 12, 4, 12, 3.0000),
        (9, 4, 0, 13, 1.1250),
        (11, 18, 0, 9, 0.6875),
        (19, 19, 6, 12, 1.5833),
        (19, 13, 13, 14, 2.3750),
        (2, 2, 10, 15, 0.1333),
        (15, 1, 3, 10, -3.7500),
        (16, 0, 12, 1, -1.0667),
        (5, 5, 13, 20, 0.2500),
        (0, 13, 4, 17, 0.0000),
        (9, 18, 3, 5, 0.6429),
        (8, 8, 10, 13, 0.6154),
        (20, 10, 6, 12, 10.0000),
        (7, 16, 2, 14, 0.3043),
        (1, 20, 20, 15, 0.0294),
        (1, 16, 16, 16, 0.0323),
        (16, 20, 4, 10, 1.1429),
        (5, 15, 13, 13, 0.2174),
        (2, 12, 20, 16, 0.0769),
        (8, 3, 20, 1, -2.0000),
        (2, 15, 16, 0, 0.1538),
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
        (12, 20, 1, 6, 1.1875),
        (7, 16, 2, 4, 1.0272),
        (16, 4, 7, 17, 0.8706),
        (4, 1, 2, 12, 0.5667),
        (17, 13, 10, 14, 0.8905),
        (18, 19, 1, 9, 1.2432),
        (20, 10, 6, 9, 1.4444),
        (6, 15, 16, 9, 0.4762),
        (2, 17, 7, 19, 0.1053),
        (19, 14, 8, 1, 9.7879),
        (13, 9, 19, 5, 1.5955),
        (1, 4, 4, 4, 0.2250),
        (8, 20, 9, 4, 1.1429),
        (0, 5, 5, 5, 0.0000),
        (10, 17, 7, 9, 0.7407),
        (9, 14, 18, 19, 0.4325),
        (13, 4, 16, 20, 0.7074),
        (10, 18, 11, 13, 0.5632),
        (6, 20, 15, 5, 0.7154),
        (3, 0, 16, 7, 0.7143),
        (8, 17, 5, 2, 2.1600),
        (1, 20, 7, 1, 0.5238),
        (4, 0, 12, 18, 0.6111),
        (0, 16, 20, 12, 0.0000),
        (7, 18, 16, 18, 0.3344),
        (8, 14, 9, 8, 0.6818),
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
        (18, 12, 12, 1, 17.6000),
        (5, 3, 0, 3, 1.2917),
        (10, 1, 17, 11, 0.8182),
        (1, 6, 3, 20, -0.8071),
        (12, 1, 9, 11, 1.0140),
        (14, 15, 13, 1, 13.4828),
        (10, 12, 14, 1, 9.4545),
        (5, 17, 9, 5, 0.2273),
        (18, 18, 18, 13, 0.8846),
        (8, 6, 16, 12, 0.2381),
        (18, 3, 19, 1, 17.8571),
        (13, 13, 3, 12, 0.5833),
        (13, 5, 8, 17, 0.4869),
        (12, 8, 16, 9, 0.9333),
        (11, 16, 11, 7, 0.9788),
        (6, 7, 17, 16, -0.1635),
        (11, 13, 10, 2, 4.9583),
        (11, 2, 1, 16, 0.5337),
        (2, 10, 13, 8, -0.5833),
        (16, 2, 16, 5, 3.0889),
        (8, 15, 9, 6, 0.6812),
        (14, 14, 2, 6, 1.8333),
        (11, 8, 15, 10, 0.6789),
        (19, 17, 5, 11, 1.2551),
        (6, 10, 18, 13, -0.1635),
        (14, 2, 14, 12, 1.0417),
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
        (9, 10, 12, 1, -0.1060),
        (1, 6, 7, 7, -0.7143),
        (5, 20, 4, 5, 0.1667),
        (1, 8, 3, 15, 1.2971),
        (4, 4, 1, 1, 0.0000),
        (12, 17, 1, 20, 0.0597),
        (6, 18, 10, 11, 1.5483),
        (8, 1, 0, 13, 0.0000),
        (18, 0, 4, 2, -0.1429),
        (10, 6, 10, 8, 2.3423),
        (16, 9, 1, 19, 0.1057),
        (11, 3, 3, 13, -0.5417),
        (10, 2, 16, 17, 0.5047),
        (18, 4, 17, 10, -21.7823),
        (2, 11, 0, 2, 0.0000),
        (18, 20, 13, 13, 0.0570),
        (4, 5, 6, 12, -0.5143),
        (5, 3, 14, 13, 0.2030),
        (4, 3, 17, 13, 0.1788),
        (19, 10, 7, 7, -0.1448),
        (16, 4, 6, 17, 0.4354),
        (14, 9, 3, 4, -0.0171),
        (4, 0, 16, 11, 0.6111),
        (0, 6, 15, 8, -0.6250),
        (1, 5, 16, 5, -0.1476),
        (12, 3, 0, 19, 0.0000),
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
        (13, 3, 20, 11, -0.0028),
        (19, 7, 1, 16, -0.0017),
        (3, 19, 16, 5, 0.0000),
        (0, 3, 9, 14, 0.0000),
        (10, 2, 2, 17, 0.0007),
        (11, 10, 20, 17, 0.0002),
        (13, 18, 2, 20, 0.0001),
        (20, 17, 11, 18, -0.0012),
        (9, 1, 11, 9, 0.9000),
        (1, 19, 10, 3, 0.0000),
        (17, 7, 18, 18, 0.0041),
        (10, 8, 4, 14, 0.0003),
        (13, 6, 1, 1, -0.0002),
        (8, 18, 1, 11, 0.0001),
        (10, 8, 0, 3, -0.0002),
        (5, 0, 19, 8, 0.6250),
        (2, 1, 6, 3, 0.0004),
        (10, 18, 10, 8, -0.0003),
        (6, 19, 19, 0, -0.0000),
        (9, 18, 1, 3, -0.0001),
        (5, 8, 6, 3, -0.0002),
        (13, 13, 4, 7, -0.0002),
        (18, 8, 17, 15, -0.0014),
        (15, 16, 7, 4, -0.0001),
        (19, 4, 6, 10, -0.0010),
        (3, 10, 13, 3, 0.2308),
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
