import pytest
from app.ciphers.binary import encode_binary, decode_binary
from app.ciphers.hexadecimal import encode_hex, decode_hex


@pytest.mark.parametrize(
    "text, expected",
    [
        ("A", "01000001"),
        ("SOS", "01010011 01001111 01010011"),
        ("", ""),
    ],
)
def test_encode_binary_casos(text, expected):
    assert encode_binary(text) == expected


@pytest.mark.parametrize(
    "binary_code, expected",
    [
        ("01000001", "A"),
        ("01010011 01001111 01010011", "SOS"),
        ("  01000001   01000010  ", "AB"),
        ("", ""),
    ],
)
def test_decode_binary_casos(binary_code, expected):
    assert decode_binary(binary_code) == expected


def test_decode_binary_invalido_lanza_value_error():
    with pytest.raises(ValueError):
        decode_binary("10201010")


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hi", "48 69"),
        ("A", "41"),
        ("", ""),
    ],
)
def test_encode_hex_casos(text, expected):
    assert encode_hex(text) == expected


@pytest.mark.parametrize(
    "hex_code, expected",
    [
        ("48 69", "Hi"),
        ("4869", "Hi"),
        ("48 6f", "Ho"),
        ("48 69 F", "Hi"),
        ("", ""),
    ],
)
def test_decode_hex_casos(hex_code, expected):
    assert decode_hex(hex_code) == expected


def test_decode_hex_invalido_lanza_value_error():
    with pytest.raises(ValueError):
        decode_hex("ZZ")
