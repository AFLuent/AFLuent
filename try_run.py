import json
from afluent import spectrum_parser

if __name__ == "__main__":
    with open("../spectrum_data.json", "r", encoding="utf-8") as infile:
        my_config = json.load(infile)

    my_spectrum = spectrum_parser.Spectrum(my_config)
    print(my_spectrum.as_dict())
