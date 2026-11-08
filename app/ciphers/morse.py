# Diccionario de equivalencias para Código Morse
MORSE_DICT = {
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',   'E': '.',
    'F': '..-.',  'G': '--.',   'H': '....',  'I': '..',    'J': '.---',
    'K': '-.-',   'L': '.-..',  'M': '--',    'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',  'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    ' ': '/'
}

# Diccionario invertido para decodificar (Morse -> Texto)
REVERSE_MORSE_DICT = {val: key for key, val in MORSE_DICT.items()}


def encode_morse(text: str) -> str:
    """Convierte texto plano a Código Morse."""
    text = text.upper()
    morse_words = []
    
    for char in text:
        if char in MORSE_DICT:
            morse_words.append(MORSE_DICT[char])
        else:
            # Si el caracter no está en el diccionario, lo ignoramos o mantenemos
            continue
            
    return " ".join(morse_words)


def decode_morse(morse_code: str) -> str:
    """Convierte Código Morse a texto plano."""
    tokens = morse_code.strip().split(" ")
    decoded_chars = []
    
    for token in tokens:
        if token in REVERSE_MORSE_DICT:
            decoded_chars.append(REVERSE_MORSE_DICT[token])
            
    return "".join(decoded_chars)