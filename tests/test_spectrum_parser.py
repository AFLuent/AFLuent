"""Include test cases on spectrum_parser module."""
import pytest
from afluent import spectrum_parser


def test_spectrum_init(test_data):
    """Check that spectrum initialization reassembles config and calculates scores."""
    input_config_dict = test_data["test_spectrum_init"]["input_config"]
    expected_output_dict = test_data["test_spectrum_init"]["output_reassembled"]
    spectrum_object = spectrum_parser.Spectrum(input_config_dict)
    assert spectrum_object.totals == expected_output_dict


def test_spectrum_init_empty_config():
    """Check that nothing will happen when empty config is passed to
    Spectrum."""
    spectrum_object = spectrum_parser.Spectrum({})
    assert not spectrum_object.reassembled_data
    assert spectrum_object.totals == {"passed": 0, "failed": 0, "skipped": 0}


def test_spectrum_generate_report_throws_error(test_data):
    """Check that error is thrown when unknown method is used."""
    config_item = test_data["test_spectrum_init"]["input_config"]
    spectrum_object = spectrum_parser.Spectrum(config_item)
    with pytest.raises(Exception):
        spectrum_object.generate_report("random")


def test_spectrum_init_eval_mode():
    config = {
        "test1": {
            "coverage": {"tests/test_data/sample_file.py": [1, 2, 3, 4]},
            "result": "passed",
        }
    }
    spectrum_object = spectrum_parser.Spectrum(config, eval_mode=True)
    assert spectrum_object.reassembled_data[
        "tests/test_data/sample_file.py"
    ].cyclomatic_complexity_data
    assert spectrum_object.reassembled_data[
        "tests/test_data/sample_file.py"
    ].logical_tiebreak_data
    assert spectrum_object.reassembled_data[
        "tests/test_data/sample_file.py"
    ].enhanced_tiebreak_data


def test_spectrum_init_enhanced_tiebreaker():
    config = {
        "test1": {
            "coverage": {"tests/test_data/sample_file.py": [1, 2, 3, 4]},
            "result": "passed",
        }
    }
    spectrum_object = spectrum_parser.Spectrum(config, tiebreaker="enhanced")
    assert not spectrum_object.reassembled_data[
        "tests/test_data/sample_file.py"
    ].cyclomatic_complexity_data
    assert not spectrum_object.reassembled_data[
        "tests/test_data/sample_file.py"
    ].logical_tiebreak_data
    assert spectrum_object.reassembled_data[
        "tests/test_data/sample_file.py"
    ].enhanced_tiebreak_data


def test_spectrum_init_logical_tiebreaker():
    config = {
        "test1": {
            "coverage": {"tests/test_data/sample_file.py": [1, 2, 3, 4]},
            "result": "passed",
        }
    }
    spectrum_object = spectrum_parser.Spectrum(config, tiebreaker="logical")
    assert not spectrum_object.reassembled_data[
        "tests/test_data/sample_file.py"
    ].cyclomatic_complexity_data
    assert spectrum_object.reassembled_data[
        "tests/test_data/sample_file.py"
    ].logical_tiebreak_data
    assert not spectrum_object.reassembled_data[
        "tests/test_data/sample_file.py"
    ].enhanced_tiebreak_data


def test_spectrum_init_cyclomatic_tiebreaker():
    config = {
        "test1": {
            "coverage": {"tests/test_data/sample_file.py": [1, 2, 3, 4]},
            "result": "passed",
        }
    }
    spectrum_object = spectrum_parser.Spectrum(config, tiebreaker="cyclomatic")
    assert spectrum_object.reassembled_data[
        "tests/test_data/sample_file.py"
    ].cyclomatic_complexity_data
    assert not spectrum_object.reassembled_data[
        "tests/test_data/sample_file.py"
    ].logical_tiebreak_data
    assert not spectrum_object.reassembled_data[
        "tests/test_data/sample_file.py"
    ].enhanced_tiebreak_data


def test_spectrum_print_report_throws_error():
    config = {
        "test1": {
            "coverage": {"tests/test_data/sample_file.py": [1, 2, 3, 4]},
            "result": "passed",
        }
    }
    spectrum_object = spectrum_parser.Spectrum(config, tiebreaker="cyclomatic")
    with pytest.raises(Exception):
        spectrum_object.print_report(["something"])


@pytest.mark.parametrize(
    "method,sus_score,rank,out_of,formatting_func",
    [
        ("tarantula", 0, 1, 1, spectrum_parser.PALETTE["safe"]),
        ("tarantula", 0.5, 1, 20, spectrum_parser.PALETTE["risky"]),
        ("tarantula", 0.5, 16, 20, spectrum_parser.PALETTE["mild"]),
        ("tarantula", 1, 8, 20, spectrum_parser.PALETTE["severe"]),
        ("ochiai", 0, 1, 1, spectrum_parser.PALETTE["safe"]),
        ("ochiai", 0.5, 1, 20, spectrum_parser.PALETTE["risky"]),
        ("ochiai", 0.5, 16, 20, spectrum_parser.PALETTE["mild"]),
        ("ochiai", 1, 8, 20, spectrum_parser.PALETTE["severe"]),
        ("dstar", 0, 1, 1, spectrum_parser.PALETTE["safe"]),
        ("dstar", 0.5, 1, 20, spectrum_parser.PALETTE["risky"]),
        ("dstar", 0.5, 16, 20, spectrum_parser.PALETTE["mild"]),
        ("dstar", float("inf"), 8, 20, spectrum_parser.PALETTE["severe"]),
    ],
)
def test_calculate_severity(method, sus_score, rank, out_of, formatting_func):
    """Check that severity calculating returns the correct formatting function."""
    assert (
        spectrum_parser.Spectrum.calculate_severity(method, sus_score, rank, out_of)
        == formatting_func
    )
