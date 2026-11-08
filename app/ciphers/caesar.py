def encrypt_caesar(text: str, shift: int) -> str:
    """Cifra un texto aplicando un desplazamiento determinado."""
    result = []
    
    for char in text:
        if char.isalpha():
            # Determinar la base según si es mayúscula o minúscula
            base = ord('A') if char.isupper() else ord('a')
            # Aplicar la fórmula del cifrado César: (c - base + shift) % 26 + base
            shifted_char = chr((ord(char) - base + shift) % 26 + base)
            result.append(shifted_char)
        else:
            # Los números, espacios y símbolos se mantienen igual
            result.append(char)
            
    return "".join(result)


def decrypt_caesar(text: str, shift: int) -> str:
    """Descifra un texto aplicando el desplazamiento inverso."""
    return encrypt_caesar(text, -shift)


def get_all_caesar_shifts(text: str) -> dict:
    """Genera las 25 posibilidades de desplazamiento para un texto dado."""
    shifts = {}
    for shift in range(1, 26):
        shifts[shift] = encrypt_caesar(text, shift)
    return shifts