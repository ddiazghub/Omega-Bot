from typing import Dict, List
from nlp import WORDS, clean
from functools import reduce

"""
Para realizar el cifrado y descifrado césar, se definió una tabla de caracteres, (Algo similar a la tabla ascii/utf-8/unicode) mediante la cual se puede transformar un caractér en un número entre 0 y n (Siendo n el número de caracteres en la tabla) y viceversa. De esta manera se organizan los caractéres causando que realizar el cifrado y descifrado se convierta en solamente sumarle el desplazamiento al valor númerico que el caractér tiene en la tabla, aplicando módulo si el valor numérico termina siendo mayor que n y sumando n si el valor termina siendo mayor que n. El valor numérico resultante de esta suma es el valor numérico del caractér desplazado.

Se hace uso de una lista para la conversión de valor numérico a caractér (El índice del carácter es su valor numérico) y de un diccionario para la conversión de caractér a valor numérico. (Los caracteres son las claves mientos que los valores numéricos son los valores del diccionario)"""

# Se define la lista para obtener un carácter a partir de su valor numérico. Primero se añaden las letras minúsculas a la lista (La función "ord" obtiene el valor numérico unicode del caractér, mientras que la función "chr" hace lo contrario, convierte un valor numérico unicode a caractér)
chars: List[str] = [chr(ord('a') + i) for i in range(26)]

# Después se añaden las mayúsculas
chars.extend((chr(ord('A') + i) for i in range(26)))

# Posteriormente se añaden los números
chars.extend((str(i) for i in range(10)))

# Al final se añaden los caractéres especiales y signos de puntuación
chars.extend((',', '.', 'á', 'é', 'í', 'ó', 'ú', '¡', '!', '¿', '?'))

# A partir de la lista, se define el diccionario para obtener el valor numérico de un carácter.
charTable: Dict[str, int] = { char: i for i, char in enumerate(chars) }

numberSwaps: Dict[str, str] = {
  '0': 'o',
  '1': 'i',
  '3': 'e',
  '4': 'a',
  '5': 's',
  '6': 'b',
  '7': 't'
}

"""
Cifra un mensaje haciendo uso de cifrado césar

Parámetros:
plainText - Mensaje en texto plano
key - Magnitud del desplazamiento

Retorna:
El mensaje cifrado
"""
def caesarEncrypt(plainText: str, key: int) -> str:
    # No se aceptan claves negativas
    if key < 0:
        raise ValueError("La clave debe ser mayor a 0")

    # Se define una lista para guardar temporalmente los caracteres del mensaje cifrado
    cipherText: List[str] = []

    # Se recorren los caracteres del mensaje
    for char in plainText:
        # Se obtiene el valor numérico del caractér haciendo uso del diccionario
        charValue = charTable.get(char)

        # Si el caractér no está en el diccionario, no se aplica desplazamiento. Se lo contrario, se le suma la clave al valor numérico y se aplica módulo para eliminar el excedente si hay. Despues se obtiene el nuevo caractér de la lista a partir del nuevo valor numérico.
        if charValue is None:
            cipherText.append(char)
        else:
            newValue = (charValue + key) % len(chars)
            cipherText.append(chars[newValue])

    # Al final se unen los caracteres de la lista y se le añade la clave al inicio del mensaje cifrado.
    return ''.join(cipherText)

"""
Descifra un mensaje cifrado mediante cifrado césar

Parámetros:
cipherText - Mensaje a descifrar

Retorna:
El mensaje en texto plano
"""
def caesarDecrypt(cipherText: str) -> str:
    # Aqui se guarda el mensaje que tiene la mayor posibilidad de ser el descifrado
    closestMatch = (-1, "", -1)

    # Se realiza una iteración para cada valor posible de la clave
    for key in range(len(chars)):
        shifted: List[str] = []

        # Se recorren los caracteres del mensaje
        for char in cipherText:
            # Se obtiene el valor numérico del caractér haciendo uso del diccionario.
            charValue = charTable.get(char)

            # Si el caractér no está en el diccionario, no se aplica desplazamiento. Se lo contrario, se le aplica primero módulo n a la clave para eliminar excedentes de esta y se resta el resultado al valor numérico. Si el resultado de esta resta es un número negativo, se le suma n. Despues se obtiene el caractér descifrado de la lista a partir del nuevo valor numérico.
            if charValue is None:
                shifted.append(char)
            else:
                newValue = (charValue - (key % len(chars)))
                newValue = newValue if newValue >= 0 else newValue + len(chars)
                shifted.append(chars[newValue])

        # Se junta el mensaje desplazado
        shifted = ''.join(shifted)

        # Se limpia y separa en palabras ignorando caracteres no alfanuméricos
        tokens = clean(shifted)

        # Se calcula una puntuación para el mensaje desplazado, dependiendo de las palabras que se encuentre en este que existan en los corpus recopilados, la puntuación del mensaje es el total de caractéres en estas palabras existentes
        score = reduce(lambda acc, word: acc + len(word) if word in WORDS else acc, tokens, 0)

        # Si la puntuación del mensaje desplazado es la mayor hasta ahora, se guarda.
        if score > closestMatch[2]:
            closestMatch = (key, shifted, score)

        print(f"Clave: {key}, Mensaje: {shifted}, Puntuación: {score}, Mensaje Limpiado: ", tokens)

    print(f"\nGanador -> Clave: {closestMatch[0]}, Mensaje: {closestMatch[1]}, Puntuación: {closestMatch[2]}", end="\n\n")

    # Se retorna el mensaje desplazado con la mayor puntuación
    return closestMatch