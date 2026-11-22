# Registro de pruebas: tabla de casos y pruebas de la IA

Proyecto: Banco y Traductor Criptográfico (traductor_cripto)
Estudiante: Angel Capacho
Fecha: 2026-11-22

## 1. Tabla de casos

### Regla: Cifrado y descifrado César (`encrypt_caesar`, `decrypt_caesar`, `get_all_caesar_shifts`)

**Regla completa (el oráculo):** Desplaza cada letra alfabética `shift` posiciones manteniendo mayúsculas y minúsculas mediante aritmética modular (`% 26`), conserva números, espacios y símbolos sin alterar, permite revertir el cifrado con `-shift` y genera las 25 variantes posibles (`1` a `25`).

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición válida | Desplazamiento estándar | `text="Hola", shift=3` | `"Krod"` | `test_encrypt_caesar_casos[Hola-3-Krod]` |
| Límite | Desbordamiento circular final del alfabeto | `text="XYZ", shift=3` | `"ABC"` | `test_encrypt_caesar_casos[XYZ-3-ABC]` |
| Límite | Desplazamiento nulo y ciclo completo | `text="Mensaje", shift=0` y `shift=26` | `"Mensaje"` | `test_encrypt_caesar_casos[Mensaje-0-Mensaje]` |
| Partición válida | Caracteres no alfabéticos conservados | `text="Hola 123!", shift=3` | `"Krod 123!"` | `test_encrypt_caesar_casos[Hola 123!-3-Krod 123!]` |
| Límite | Cadena vacía | `text="", shift=5` | `""` | `test_encrypt_caesar_casos[-5-]` |
| Propiedad inversa | Descifrado revierte el cifrado | `text="Seguridad Informatica 2026!", shift=7` | Texto original exacto | `test_decrypt_caesar_invierte_cifrado` |
| Límite | Rango completo de combinaciones | `text="ABC"` | Diccionario con claves `1..25` | `test_get_all_caesar_shifts_genera_25_variantes` |

**Ambigüedades encontradas:** Python considera `char.isalpha() == True` para letras con tilde o `ñ`, pero la fórmula `(ord(char) - base + shift) % 26` asume alfabeto inglés ASCII de 26 letras (`A-Z`). Se resolvió acotando las pruebas al alfabeto ASCII estándar definido por el módulo.

---

### Regla: Codificación y decodificación Morse (`encode_morse`, `decode_morse`)

**Regla completa (el oráculo):** Convierte letras (`A-Z`), dígitos (`0-9`) y espacios (`/`) a código Morse separados por espacio simple, ignorando caracteres fuera del diccionario; en sentido inverso reconstruye el texto plano a partir de tokens Morse válidos.

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición válida | Palabra estándar en mayúsculas | `"SOS"` | `"... --- ..."` | `test_encode_morse_casos[SOS-... --- ...]` |
| Partición válida | Normalización de minúsculas | `"hola"` | `".... --- .-.. .-"` | `test_encode_morse_casos[hola-.... --- .-.. .-]` |
| Partición válida | Separador de palabras y números | `"HI 5"` | `".... .. / ....."` | `test_encode_morse_casos[HI 5-.... .. / .....]` |
| Partición límite | Símbolos no soportados ignorados | `"SOS!?"` | `"... --- ..."` | `test_encode_morse_casos[SOS!?-... --- ...]` |
| Límite | Cadena vacía | `""` | `""` | `test_encode_morse_casos[-]` |
| Partición válida | Decodificación con espacios extra y token desconocido | `".- ??? -..."` | `"AB"` | `test_decode_morse_casos[.- ??? -...-AB]` |

**Ambigüedades encontradas:** La especificación no indicaba si los símbolos de puntuación debían lanzar error o ignorarse; según la implementación en `morse.py`, se omiten silenciosamente (`continue`), comportamiento fijado en las pruebas.

---

### Regla: Codificación y decodificación Binaria y Hexadecimal (`encode_binary`, `decode_binary`, `encode_hex`, `decode_hex`)

**Regla completa (el oráculo):** Convierte cada carácter a su representación ASCII de 8 bits (`08b`) o 2 dígitos hexadecimales en mayúsculas (`02X`) separados por espacio, y decodifica cadenas válidas lanzando `ValueError` ante caracteres fuera de base 2 o base 16.

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición válida | Codificación binaria de 8 bits | `"A"` | `"01000001"` | `test_encode_binary_casos[A-01000001]` |
| Partición válida | Decodificación binaria con espacios múltiples | `"  01000001   01000010  "` | `"AB"` | `test_decode_binary_casos[  01000001   01000010  -AB]` |
| Partición inválida | Dígito no binario (`2`) | `"10201010"` | `ValueError` | `test_decode_binary_invalido_lanza_value_error` |
| Partición válida | Codificación y decodificación hexadecimal | `"Hi"` / `"4869"` | `"48 69"` / `"Hi"` | `test_encode_hex_casos`, `test_decode_hex_casos` |
| Límite | Nibble impar al final de cadena hex | `"48 69 F"` | `"Hi"` | `test_decode_hex_casos[48 69 F-Hi]` |
| Partición inválida | Caracteres fuera de base 16 | `"ZZ"` | `ValueError` | `test_decode_hex_invalido_lanza_value_error` |

**Ambigüedades encontradas:** Cuando una cadena hexadecimal tiene longitud impar (ej. `"48 69 F"`), `decode_hex` descarta el último carácter suelto (`if len(pair) == 2`) en lugar de fallar. Se documentó y cubrió como caso límite.

---

### Regla: Sustitución Monoalfabética (`encrypt_substitution`, `decrypt_substitution`)

**Regla completa (el oráculo):** Cifra o descifra usando una clave de exactamente 26 caracteres únicos; si la longitud es distinta de 26 o tiene caracteres repetidos, lanza `ValueError` (HTTP 400 en la API).

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición válida | Clave válida de 26 letras únicas | `text="Hola Mundo 2026!", key="QWERTYUIOPASDFGHJKLZXCVBNM"` | `"Igsq Dxfrg 2026!"` | `test_substitution_cifrado_y_descifrado_valido` |
| Límite | Clave en minúsculas con espacios laterales | `key="  qwertyuiopasdfghjklzxcvbnm  "` | Normaliza y cifra `"ABC"` -> `"QWE"` | `test_substitution_normaliza_clave_con_espacios_y_minusculas` |
| Partición inválida | Clave vacía o corta | `key=""` / `key="ABC"` | `ValueError` | `test_substitution_clave_invalida_lanza_value_error` |
| Partición inválida | Clave de 26 caracteres con letras repetidas | `key="QWERTYUIOPASDFGHJKLZXCVBNN"` | `ValueError` | `test_substitution_clave_invalida_lanza_value_error` |

**Ambigüedades encontradas:** La validación verifica `len(key_alphabet) != 26 or len(set(key_alphabet)) != 26`, sin exigir `.isalpha()`. Se mantuvieron claves alfabéticas en las pruebas y se registró esta observación para futura mejora de validación.

---

### Regla: Detector Inteligente de Patrones (`detect_code_type`)

**Regla completa (el oráculo):** Analiza una cadena limpia y retorna todos los formatos compatibles (`Morse`, `Binario`, `Hexadecimal`, `Texto Plano / Cifrado César / Sustitución`) con su nivel de confianza y explicación; si la cadena está vacía o solo tiene espacios, retorna `{"matches": []}`.

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Límite | Texto vacío o solo espacios | `""`, `"   "` | `{"matches": []}` | `test_detect_code_type_vacio` |
| Partición válida | Solo puntos, rayas, espacios y `/` | `"... --- ... / .-"` | Coincide `Morse` (`Alta`) | `test_detect_code_type_morse` |
| Límite | Binario múltiplo de 8 bits | `"01000001"` | `Binario` (`Alta`) y `Hexadecimal` (`Alta`) | `test_detect_code_type_binario_8bits` |
| Límite | Binario no múltiplo de 8 bits | `"0101"` | `Binario` (`Media`) | `test_detect_code_type_binario_no_multiplo_de_8` |
| Partición válida | Pares hexadecimales con letras | `"48 69"` | `Hexadecimal` (`Alta`) | `test_detect_code_type_hexadecimal` |
| Partición válida | Texto alfabético | `"Hola mundo"` | `Texto Plano / Cifrado César / Sustitución` (`Alta`) | `test_detect_code_type_texto_alfabetico` |

#### Tabla de decisión del detector

| Condición de entrada | Morse | Binario | Hexadecimal | Texto Plano / César / Sustitución |
|---|---|---|---|---|
| Vacío o solo espacios | No | No | No | No (`matches: []`) |
| Solo `.`, `-`, `/`, espacios | Sí (`Alta`) | No | No | No |
| Solo `0`, `1`, espacios (longitud sin espacios múltiplo de 8) | No | Sí (`Alta`) | Sí (`Alta`, si longitud par >= 2) | No |
| Solo `0`, `1`, espacios (longitud no múltiplo de 8) | No | Sí (`Media`) | Sí (si longitud par) / No (si impar) | No |
| `0-9`, `A-F`, espacios (longitud par) | No | No | Sí (`Alta`) | Sí (si contiene `A-F`) / No (si solo `0-9`) |
| Contiene letras `G-Z` o `g-z` | No | No | No | Sí (`Alta`) |

## 2. Pruebas de la IA descartadas o corregidas

**Prompt usado:** Generación de suite de pruebas unitarias y de API en `pytest` con casos borde y parametrización para los módulos de `app/ciphers/`, `app/detector/` y `app/main.py` (ver Fase 3 y Fase 5 de `BitacorausoIA.txt`).

| Prueba generada | Decisión | Por qué | En su lugar |
|---|---|---|---|
| `test_caesar_retorna_algo`: `assert encrypt_caesar("Hola", 3) is not None` | Descartada | Aserción débil: pasa incluso si la función devuelve una cadena vacía o errónea. | `assert encrypt_caesar("Hola", 3) == "Krod"` |
| `test_substitution_cifrado`: esperaba `"Igsq Dxfeg 2026!"` para `"Hola Mundo 2026!"` con clave QWERTY | Corregida | Cálculo manual erróneo de la IA al mapear la letra `'d'` (índice 3 -> `'r'`, no `'e'`). | `assert cifrado == "Igsq Dxfrg 2026!"` |
| `test_detector_solo_binario`: esperaba únicamente `"Binario"` para `"01000001"` | Corregida | La regla del detector evalúa coincidencias múltiples y `"01000001"` también es hexadecimal válido de longitud par. | Verificar que tanto `"Binario"` como `"Hexadecimal"` estén presentes en `matches`. |
| `test_ui_colores_css`: intentaba validar estilos CSS desde Python | Descartada | No prueba lógica de negocio ni contratos de API; pertenece a revisión visual manual. | Pruebas de integración HTTP con `TestClient` sobre los endpoints JSON en `tests/test_api.py`. |

**Decisión:** Conservada, Corregida o Descartada.

## 3. Romper el código a propósito

| Cambio introducido | Archivo y línea | ¿Alguna prueba falló? | Qué hice |
|---|---|---|---|
| Cambiar `% 26` por `% 25` en el cálculo del desplazamiento | `app/ciphers/caesar.py:10` | Sí, `test_encrypt_caesar_casos[XYZ-3-ABC]` | Revertí el cambio; la prueba protege el desbordamiento circular del alfabeto. |
| Cambiar `len(key_alphabet) != 26` por `len(key_alphabet) < 26` | `app/ciphers/substitution.py:9` | Sí, `test_substitution_clave_invalida_lanza_value_error` | Revertí el cambio; la validación de longitud exacta quedó cubierta. |
| Invertir condición `len(...) % 8 == 0` a `!= 0` en confianza binaria | `app/detector/detector.py:21` | Sí, `test_detect_code_type_binario_8bits` | Revertí el cambio; la suite detecta de inmediato la degradación en la confianza del detector. |

## 4. Datos de prueba

**Origen:** sintéticos escritos a mano y generados con asistencia de IA. Confirmo que no hay datos de personas reales.

**Casos difíciles incluidos:** cadenas vacías y solo espacios (`""`, `"   "`, `"\n\t"`), desbordamiento circular al final del alfabeto (`"XYZ"` -> `"ABC"`), desplazamientos límite (`0`, `26` y negativos `-3`), símbolos no soportados en Morse (`"SOS!?"`), tokens desconocidos en Morse (`".- ??? -..."`), dígitos inválidos en binario (`"10201010"`), caracteres inválidos y nibble impar en hexadecimal (`"ZZ"`, `"48 69 F"`), claves de sustitución con espacios/minúsculas o letras repetidas, y entradas ambiguas (`"01000001"`) que activan múltiples reglas en el detector.