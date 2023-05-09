from typing import List
from itertools import chain
from nltk.corpus import wordnet, words, names, stopwords, cess_esp, conll2002
from nltk.tokenize import regexp_tokenize
import re
"""
Se limpian y separan un conjunto de palabras, transformándo todos sus caracteres en minúscula y reemplazando variantes de letra por su forma original ascii.
"""


def clean(word: str) -> List[str]:
    return regexp_tokenize(substitute(word.lower()),
                           r"[a-zA-Z:\u00C0-\u00FF]+")


"""
Se reemplazan variantes de letras por su forma original ascii y números por la letra a la cual más se asemejan.
"""


def substitute(word: str) -> str:
    return re.sub(REGEX, lambda match: SUBSTITUTIONS[match.lastindex - 1][1],
                  word)


"""
Se limpian y separan un conjunto de palabras, transformándo todos sus caracteres en minúscula y reemplazando variantes de letra por su forma original ascii. También se deshace de palabras compuestas por solamente 1 letra.
"""


def clean2(word: str) -> List[str]:
    return (token for token in regexp_tokenize(substitute(
        word.lower()), r"[a-zA-Z:\u00C0-\u00FF]+") if len(token) > 1)


"""
Se reemplazan variantes de letras por su forma original ascii.
"""


def substitute2(word: str) -> str:
    return re.sub(REGEX, lambda match: SUBSTITUTIONS2[match.lastindex - 1][1],
                  word)


"""
Tupla que contiene patrones y los caracteres por los cuales se reemplazan
"""
SUBSTITUTIONS = (("(0|ð|ò|ó|ô|õ|ö)", 'o'), ("(1|ì|í|î|ï)", 'i'),
                 ("(3|è|é|ê|ë)", 'e'), ("(4|@|à|á|â|ã|ä|å)",
                                        'a'), ("(6)", 'b'), ("(7)", 't'),
                 ("(ù|ú|û|ü)", 'u'), ("(æ)", "ae"), ("(ñ)", 'n'))
"""
Tupla que contiene patrones y los caracteres por los cuales se reemplazan
"""
SUBSTITUTIONS2 = (("(ð|ò|ó|ô|õ|ö)", 'o'), ("(ì|í|î|ï)", 'i'),
                  ("(è|é|ê|ë)", 'e'), ("(à|á|â|ã|ä|å)",
                                       'a'), ("(ù|ú|û|ü)", 'u'), ("(ñ)", 'n'))

print("Cargando corpus linguístico... (Este proceso se puede demorar un rato)")
"""
Expresión regular para reemplazar caracteres especiales
"""
REGEX = re.compile('|'.join(substitution[0] for substitution in SUBSTITUTIONS))
"""
Se recopilan palabras de distintos corpus linguísticos de nltk en un conjunto, este conjunto se utilizará para validar los mensajes cuando se estén decifrando
"""
WORDS = {
    cleanedWord
    for word in chain(wordnet.words("spa"), words.words(), names.words(
    ), stopwords.words("spanish"), cess_esp.words(), conll2002.words())
    for cleanedWord in clean2(word)
}

print("Iniciando programa...", end="\n\n")
