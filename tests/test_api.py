import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
VALID_KEY = "QWERTYUIOPASDFGHJKLZXCVBNM"


def test_endpoint_home():
    res = client.get("/")
    assert res.status_code == 200
    assert "mensaje" in res.json()


def test_endpoints_caesar():
    enc = client.post("/api/caesar/encrypt", json={"text": "Hola", "shift": 3})
    assert enc.status_code == 200
    assert enc.json() == {"result": "Krod"}

    dec = client.post("/api/caesar/decrypt", json={"text": "Krod", "shift": 3})
    assert dec.status_code == 200
    assert dec.json() == {"result": "Hola"}

    all_s = client.post("/api/caesar/all-shifts", json={"text": "ABC"})
    assert all_s.status_code == 200
    assert all_s.json()["shifts"]["3"] == "DEF"


def test_endpoints_morse_binary_hex():
    assert client.post("/api/morse/encode", json={"text": "SOS"}).json() == {"result": "... --- ..."}
    assert client.post("/api/morse/decode", json={"text": "... --- ..."}).json() == {"result": "SOS"}
    assert client.post("/api/binary/encode", json={"text": "A"}).json() == {"result": "01000001"}
    assert client.post("/api/binary/decode", json={"text": "01000001"}).json() == {"result": "A"}
    assert client.post("/api/hex/encode", json={"text": "Hi"}).json() == {"result": "48 69"}
    assert client.post("/api/hex/decode", json={"text": "48 69"}).json() == {"result": "Hi"}


def test_endpoints_substitution_valido_e_invalido():
    ok = client.post("/api/substitution/encrypt", json={"text": "ABC", "key": VALID_KEY})
    assert ok.status_code == 200
    assert ok.json() == {"result": "QWE"}

    bad = client.post("/api/substitution/encrypt", json={"text": "ABC", "key": "CLAVE_CORTA"})
    assert bad.status_code == 400
    assert "26 letras" in bad.json()["detail"]


def test_endpoint_detector_y_catalog():
    det = client.post("/api/detector/analyze", json={"text": "... --- ..."})
    assert det.status_code == 200
    assert det.json()["matches"][0]["type"] == "Morse"

    cat = client.get("/api/catalog")
    assert cat.status_code == 200
    assert isinstance(cat.json(), list)
