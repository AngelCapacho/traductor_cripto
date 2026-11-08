def encode_hex(text: str) -> str:
    """Convierte texto plano a representación Hexadecimal."""
    # format(ord(char), '02X') convierte la letra a hex de 2 dígitos en mayúsculas
    return " ".join(format(ord(char), '02X') for char in text)


def decode_hex(hex_code: str) -> str:
    """Convierte una cadena Hexadecimal a texto plano."""
    # Eliminar espacios si los hay
    clean_hex = hex_code.replace(" ", "")
    decoded_chars = []
    
    # Procesar de a 2 caracteres hexadecimales
    for i in range(0, len(clean_hex), 2):
        pair = clean_hex[i:i+2]
        if len(pair) == 2:
            decoded_chars.append(chr(int(pair, 16)))
            
    return "".join(decoded_chars)