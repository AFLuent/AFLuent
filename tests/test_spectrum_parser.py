"""Include test cases on spectrum_parser module."""
from afluent import spectrum_parser
import pytest


def test_spectrum_init(test_data):
    """Check that spectrum initialization reassembles config and calculates scores."""
    input_config_list = test_data["test_spectrum_init"]["input_config"]
    expected_output_list = test_data["test_spectrum_init"]["output_reassembled"]
    for test_index in range(len(input_config_list)):
        config_item = input_config_list[test_index]
        spectrum_object = spectrum_parser.Spectrum(config_item)
        assert spectrum_object.as_dict() == expected_output_list[test_index]


def test_spectrum_init_empty_config():
    """Check that nothing will happen when empty config is passed to
    Spectrum."""
    spectrum_object = spectrum_parser.Spectrum({})
    assert spectrum_object.reassembled_data == {}
    assert spectrum_object.totals == {"passed": 0, "failed": 0, "skipped": 0}


# TODO: unclear which tied lines will be placed first
# def test_spectrum_generate_report(test_data):
#     """Check that reports are correctly generated."""
#     config_item = test_data["test_spectrum_init"]["input_config"][0]
#     spectrum_object = spectrum_parser.Spectrum(config_item)
#     report_output = spectrum_object.generate_report("ochiai")
#     expected_report = {}
#     assert True


def test_spectrum_generate_report_throws_error(test_data):
    """Check that error is thrown when unknown method is used."""
    config_item = test_data["test_spectrum_init"]["input_config"][0]
    spectrum_object = spectrum_parser.Spectrum(config_item)
    with pytest.raises(Exception):
        spectrum_object.generate_report("random")


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
        ("dstar", 999999999, 8, 20, spectrum_parser.PALETTE["severe"]),
    ],
)
def test_calculate_severity(method, sus_score, rank, out_of, formatting_func):
    assert (
        spectrum_parser.Spectrum.calculate_severity(method, sus_score, rank, out_of)
        == formatting_func
    )
