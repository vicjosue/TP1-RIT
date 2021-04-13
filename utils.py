# Author: Victor Camacho Artavia <joscamachoartavia@gmail.com>,
#         Jimmy Mok Zhgen <jimmymokz14@gmail.com>

import re
import unicodedata

def process_line(line,stopwords):
    """
    Deletes stopwords, lower the letters, detele backspaces and non usable words.

    Parameters
    ----------
    line: str
        String to be processed and converted to words.
    stopwords: list
        List with all stopwords to be handled.

    
    Returns
    -------
    processed_words: list
        List of processed words.
    """
    processed_words=[]
    words=line.split()
    is_word_splitted=False
    splitted_word=""

    for word in words:
        if(word=="OPTIONS"):
            processed_words.append(word)
        if word=="DESCRIPTION" or word=="DESCRIPCI�N": # spanish or english
            processed_words.append(word)
        if(check_point(word)): # '.hola' or 'hola.'
            continue

        word=splitpoints(word) # hello.two
        for w in word[1:]:
            words.append(w)
        word=word[0]
        word = double_line(word)

        if word[0] == "":
            continue
        if(type(word)==list):
            words.append(word[1])
            word=word[0]

        word = normalize(word) # lower, accent
        if(word[-1]=="-"):
            is_word_splitted=True
            splitted_word=word[:-1]
            continue

        if(is_word_splitted):
            word=splitted_word+word
            is_word_splitted=False

        if(word in stopwords):
            continue #don't do anything, they are not valuable
        word = delete_backspace(word)
        word = delete_characters(word)

        processed_words.append(word)
    return processed_words

def delete_backspace(line): #https://stackoverflow.com/a/34364138/14494755
    """
    Delete backspaces on a line

    Parameters
    ----------
    line: str
        line to delete backspaces
    
    Returns
    -------
    processed_words: list
        List of proccesed words.
    """
    return re.sub('\b+', '', line)

def normalize(text):
    #Funcion: este metodo sirve para normalizar el texto que se recibe.
    #Parametros: String.
    #Resultado: String normalizado de acuerdo a los criterios.

    text_lower = text.lower()
    #print(text_unaccent + "hola")
    text_unaccent = ''.join((c for c in unicodedata.normalize('NFD', text_lower) if unicodedata.category(c) != 'Mn'))
    return text_unaccent  

def remove_accent(text):
    #Funcion: este metodo sirve para remover tildes y dieresis.
    #Parametros: String.
    #Resultado: String sin acentos.

    replacements = (
        ["á", "a"],
        ["é", "e"],
        ["í", "i"],
        ["ó", "o"],
        ["ú", "u"],
        ["ä", "a"],
        ["ë", "e"],
        ["ï", "i"],
        ["ö", "o"],
        ["ü", "u"]
    )
    for accent_letter, letter in replacements:
        
        text = text.replace(accent_letter,letter)

    return text

def read_stopwords(file_name):
    #Funcion: este metodo carga y enlista los stopwords.
    #Parametros: No hay.
    #Resultado: Lista de stopwords
    stopwords = []

    with open(file_name) as f:
        for line in f:
            stopwords.append(line.split()[0])
    return stopwords


def check_point(word):
    #Funcion: este metodo revisa los terminos con el signo punto.
    #Parametros: Palabra o string
    #Resultado: Booleano
    if word[0] == "." or word[-1] == ".":
        return True
    if ".." in word:
        return True
    return False
        
def double_line(word):
    #Funcion: Maneja el caso "--".
    #Parametros: Palabra o string
    #Resultado: Lista con terminos
    if len(word) <= 1:
        return word
    if word[0] == "-" and word[1] == "-":
        return [word[2:],"@" + word[2:]]
    return word


def splitpoints(word):
    #Funcion: Divide las palabras con puntos y elimina los que son solo numeros.
    #Parametros: Palabra o string
    #Resultado: Lista con terminos.

    x = re.search("[a-zA-Z]", word)
    word_splited = []
    result = [word]
    if "." in word:
        if x:
            word_splited = word.split(".")
        for i in word_splited:
            if i.isnumeric()==False:
                result.append(i)
    return result

def delete_characters(word):
    #Funcion: Revisa letra por letra de una palabra para solo dejar pasar los caracteres de palabras
    #Parametros: Palabra.
    #Resultado: Palabra procesada.
    final_word = ""
    for letter in word:
        pattern = re.compile("[a-z0-9ñ_.]")
        if pattern.match(letter) is not None:
            final_word+=letter
    return final_word