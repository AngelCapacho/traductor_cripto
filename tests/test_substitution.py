import pytest
from app.ciphers.substitution import encrypt_substitution, decrypt_substitution

VALID_KEY = "QWERTYUIOPASDFGHJKLZXCVBNM"


def test_substitution_cifrado_y_descifrado_valido():
    original = "Hola Mundo 2026!"
    cifrado = encrypt_substitution(original, VALID_KEY)
    assert cifrado == "Igsq Dxfeg 2026!"
    assert decrypt_substitution(cifrado, VALID_KEY) == original


def test_substitution_normaliza_clave_con_espacios_y_minusculas():
    key_lower = "  qwertyuiopasdfghjklzxcvbnm  "
    assert encrypt_substitution("ABC", key_lower) == "QWE"


@pytest.mark.parametrize(
    "bad_key",
    [
        "",
        "ABC",
        "AAAAAAAAAAAAAAAAAAAAAAAAAA",
        "QWERTYUIOPASDFGHJKLZXCVBNN",
    ],
)
def test_substitution_clave_invalida_lanza_value_error(bad_key):
    with pytest.raises(ValueError):
        encrypt_substitution("Hola", bad_key)
    with pytest.raises(ValueError):
        decrypt_substitution("Hola", bad_key)
