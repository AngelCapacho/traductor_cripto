import string

STANDARD_ALPHABET = string.ascii_uppercase

def encrypt_substitution(text: str, key_alphabet: str) -> str:
    """Cifra un texto usando un alfabeto de sustitución personalizado de 26 letras."""
    key_alphabet = key_alphabet.upper().strip()
    
    # Validar que la clave tenga exactamente 26 letras únicas
    if len(key_alphabet) != 26 or len(set(key_alphabet)) != 26:
        raise ValueError("La clave debe contener exactamente las 26 letras del alfabeto sin repetir.")
        
    translation_table = str.maketrans(
        STANDARD_ALPHABET + STANDARD_ALPHABET.lower(),
        key_alphabet + key_alphabet.lower()
    )
    return text.translate(translation_table)


def decrypt_substitution(text: str, key_alphabet: str) -> str:
    """Descifra un texto revertiendo el alfabeto de sustitución."""
    key_alphabet = key_alphabet.upper().strip()
    
    if len(key_alphabet) != 26 or len(set(key_alphabet)) != 26:
        raise ValueError("La clave debe contener exactamente las 26 letras del alfabeto sin repetir.")
        
    translation_table = str.maketrans(
        key_alphabet + key_alphabet.lower(),
        STANDARD_ALPHABET + STANDARD_ALPHABET.lower()
    )
    return text.translate(translation_table)