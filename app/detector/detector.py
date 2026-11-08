import re

def detect_code_type(text: str) -> dict:
    """
    Analiza un texto y devuelve una lista de posibles formatos detectados con sus explicaciones.
    """
    clean_text = text.strip()
    matches = []
    
    if not clean_text:
        return {"matches": []}

    # 1. Patrón Código Morse (solo Puntos, Rayas, Espacios y Barras)
    if re.fullmatch(r'[\.\-\s\/]+', clean_text):
        matches.append({
            "type": "Morse",
            "confidence": "Alta",
            "reason": "El texto contiene únicamente puntos (.), rayas (-), espacios y diagonales (/)."
        })

    # 2. Patrón Binario (solo 0s, 1s y espacios)
    if re.fullmatch(r'[01\s]+', clean_text):
        matches.append({
            "type": "Binario",
            "confidence": "Alta" if len(clean_text.replace(" ", "")) % 8 == 0 else "Media",
            "reason": "El texto está compuesto exclusivamente por ceros (0), unos (1) y espacios."
        })

    # 3. Patrón Hexadecimal (caracteres 0-9, A-F, a-f y espacios)
    clean_hex = clean_text.replace(" ", "")
    if re.fullmatch(r'[0-9A-Fa-f\s]+', clean_text) and len(clean_hex) % 2 == 0:
        matches.append({
            "type": "Hexadecimal",
            "confidence": "Alta" if len(clean_hex) >= 2 else "Media",
            "reason": "Contiene valores alfanuméricos válidos en base 16 (0-9, A-F) con longitud par."
        })

    # 4. Texto Plano o Cifrado César / Sustitución
    if re.search(r'[a-zA-Z]', clean_text):
        matches.append({
            "type": "Texto Plano / Cifrado César / Sustitución",
            "confidence": "Alta",
            "reason": "Contiene caracteres alfabéticos. Podría ser un mensaje legible en texto plano o un texto cifrado mediante desplazamientos César o sustitución."
        })

    return {"matches": matches}