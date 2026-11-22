import pytest
from app.detector.detector import detect_code_type


@pytest.mark.parametrize("empty_input", ["", "   ", "\n\t"])
def test_detect_code_type_vacio(empty_input):
    assert detect_code_type(empty_input) == {"matches": []}


def test_detect_code_type_morse():
    result = detect_code_type("... --- ... / .-")
    types = {m["type"]: m for m in result["matches"]}
    assert "Morse" in types
    assert types["Morse"]["confidence"] == "Alta"


def test_detect_code_type_binario_8bits():
    result = detect_code_type("01000001")
    types = {m["type"]: m for m in result["matches"]}
    assert "Binario" in types
    assert types["Binario"]["confidence"] == "Alta"
    assert "Hexadecimal" in types


def test_detect_code_type_binario_no_multiplo_de_8():
    result = detect_code_type("0101")
    types = {m["type"]: m for m in result["matches"]}
    assert "Binario" in types
    assert types["Binario"]["confidence"] == "Media"


def test_detect_code_type_hexadecimal():
    result = detect_code_type("48 69")
    types = {m["type"]: m for m in result["matches"]}
    assert "Hexadecimal" in types
    assert types["Hexadecimal"]["confidence"] == "Alta"


def test_detect_code_type_texto_alfabetico():
    result = detect_code_type("Hola mundo")
    types = {m["type"]: m for m in result["matches"]}
    assert "Texto Plano / Cifrado César / Sustitución" in types
    assert types["Texto Plano / Cifrado César / Sustitución"]["confidence"] == "Alta"
