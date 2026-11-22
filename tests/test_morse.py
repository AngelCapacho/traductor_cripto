import pytest
from app.ciphers.morse import encode_morse, decode_morse


@pytest.mark.parametrize(
    "text, expected",
    [
        ("SOS", "... --- ..."),
        ("hola", ".... --- .-.. .-"),
        ("HI 5", ".... .. / ....."),
        ("SOS!?", "... --- ..."),
        ("", ""),
    ],
)
def test_encode_morse_casos(text, expected):
    assert encode_morse(text) == expected


@pytest.mark.parametrize(
    "morse_code, expected",
    [
        ("... --- ...", "SOS"),
        (".... .. / .....", "HI 5"),
        ("  .- -...  ", "AB"),
        (".- ??? -...", "AB"),
        ("", ""),
    ],
)
def test_decode_morse_casos(morse_code, expected):
    assert decode_morse(morse_code) == expected
