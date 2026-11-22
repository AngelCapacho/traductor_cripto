import pytest
from app.ciphers.caesar import encrypt_caesar, decrypt_caesar, get_all_caesar_shifts


@pytest.mark.parametrize(
    "text, shift, expected",
    [
        ("Hola", 3, "Krod"),
        ("XYZ", 3, "ABC"),
        ("xyz", 3, "abc"),
        ("Hola 123!", 3, "Krod 123!"),
        ("Mensaje", 0, "Mensaje"),
        ("Mensaje", 26, "Mensaje"),
        ("Krod", -3, "Hola"),
        ("", 5, ""),
    ],
)
def test_encrypt_caesar_casos(text, shift, expected):
    assert encrypt_caesar(text, shift) == expected


def test_decrypt_caesar_invierte_cifrado():
    original = "Seguridad Informatica 2026!"
    cifrado = encrypt_caesar(original, 7)
    assert cifrado != original
    assert decrypt_caesar(cifrado, 7) == original


def test_get_all_caesar_shifts_genera_25_variantes():
    shifts = get_all_caesar_shifts("ABC")
    assert len(shifts) == 25
    assert list(shifts.keys()) == list(range(1, 26))
    assert shifts[3] == "DEF"
    assert shifts[25] == "ZAB"
