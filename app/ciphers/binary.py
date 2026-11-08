def encode_binary(text: str) -> str:
    """Convierte texto plano a código binario de 8 bits por carácter."""
    # format(ord(char), '08b') convierte cada letra a un binario de 8 ceros/unos
    return " ".join(format(ord(char), '08b') for char in text)


def decode_binary(binary_code: str) -> str:
    """Convierte cadenas de código binario separadas por espacios a texto plano."""
    binary_values = binary_code.strip().split(" ")
    decoded_chars = []
    
    for b in binary_values:
        if b:
            # int(b, 2) convierte la cadena base 2 a entero, y chr() a su letra ASCII
            decoded_chars.append(chr(int(b, 2)))
            
    return "".join(decoded_chars)