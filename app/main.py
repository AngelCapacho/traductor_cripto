from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.ciphers.morse import encode_morse, decode_morse
from app.ciphers.caesar import encrypt_caesar, decrypt_caesar, get_all_caesar_shifts
from app.ciphers.binary import encode_binary, decode_binary
from app.ciphers.hexadecimal import encode_hex, decode_hex
from app.ciphers.substitution import encrypt_substitution, decrypt_substitution
from app.detector.detector import detect_code_type

app = FastAPI(title="Banco y Traductor Criptográfico")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Modelos de datos
class TextRequest(BaseModel):
    text: str

class CaesarRequest(BaseModel):
    text: str
    shift: int

class SubstitutionRequest(BaseModel):
    text: str
    key: str

@app.get("/")
def home():
    return {"mensaje": "Backend del Banco y Traductor Criptográfico listo y organizado"}

# --- Morse ---
@app.post("/api/morse/encode")
def api_encode_morse(request: TextRequest):
    return {"result": encode_morse(request.text)}

@app.post("/api/morse/decode")
def api_decode_morse(request: TextRequest):
    return {"result": decode_morse(request.text)}

# --- César ---
@app.post("/api/caesar/encrypt")
def api_encrypt_caesar(request: CaesarRequest):
    return {"result": encrypt_caesar(request.text, request.shift)}

@app.post("/api/caesar/decrypt")
def api_decrypt_caesar(request: CaesarRequest):
    return {"result": decrypt_caesar(request.text, request.shift)}

@app.post("/api/caesar/all-shifts")
def api_caesar_all_shifts(request: TextRequest):
    return {"shifts": get_all_caesar_shifts(request.text)}

# --- Binario ---
@app.post("/api/binary/encode")
def api_encode_binary(request: TextRequest):
    return {"result": encode_binary(request.text)}

@app.post("/api/binary/decode")
def api_decode_binary(request: TextRequest):
    return {"result": decode_binary(request.text)}

# --- Hexadecimal ---
@app.post("/api/hex/encode")
def api_encode_hex(request: TextRequest):
    return {"result": encode_hex(request.text)}

@app.post("/api/hex/decode")
def api_decode_hex(request: TextRequest):
    return {"result": decode_hex(request.text)}

# --- Sustitución Simple ---
@app.post("/api/substitution/encrypt")
def api_encrypt_substitution(request: SubstitutionRequest):
    try:
        return {"result": encrypt_substitution(request.text, request.key)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/substitution/decrypt")
def api_decrypt_substitution(request: SubstitutionRequest):
    try:
        return {"result": decrypt_substitution(request.text, request.key)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Detector Inteligente ---
@app.post("/api/detector/analyze")
def api_analyze_code(request: TextRequest):
    return detect_code_type(request.text)

import json

# --- Endpoint para el Catálogo Educativo ---
@app.get("/api/catalog")
def api_get_catalog():
    try:
        with open("app/data/catalog.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        return []