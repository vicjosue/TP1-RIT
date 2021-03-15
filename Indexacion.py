from os import walk
import math
import re

def indexColection():

    root = input("Ingrese la ruta completa del archivo: ")
    nombre = root.split("/")[-1]

    cont_files = 0
    documents = {}
    vocabulary = {}
    stopwords = read_stopwords()

    is_word_splitted=False
    splitted_word=""
    
    
    for (dirpath, dirs, files) in walk(root):
        relative_path='.'+ dirpath.split(root)[-1] + '\\'
        for file in files:
            with open(dirpath+'\\'+file, "rt", encoding='utf8') as file:

                documents[cont_files]= {'path': relative_path,'name':file.name.split("\\")[-1], 'pairs': {}}
                cont_words = 0
                cont_description_words=0
                description=""
                for line in file:
                    for word in line.split():
                        word=splitpoints(word) # hello.two
                        for w in word[1:]:
                            line.append(w)
                        word=word[0]

                        word = double_line(word)
                        if(type(word)==list):
                            line.append(word[1])
                            word=word[0]

                        word = normalize(word) # lower, accent
                        if(word[-1]=="-"):
                            is_word_splitted=True
                            splitted_word=word[:-1]
                            continue

                        if(is_word_splitted):
                            word=splitted_word+word
                            is_word_splitted=False

                        if(check_point(word)): # '.hola' or 'hola.'
                            continue

                        if(word in stopwords):
                            continue #don't do anything, they are not valuable

                        if word=="DESCRIPTION" and cont_description_words<=200:
                            if(word=="OPTIONS"):
                                cont_description_words=201
                            else:
                                description+=word+" "
                        cont_words = cont_words + 1

                        if(word not in documents[cont_files]['pairs']):
                            documents[cont_files]['pairs'][word] = 1
                            updateVocabulary(vocabulary,word)

                        else:
                            documents[cont_files]['pairs'][word] = documents[cont_files]['pairs'][word]+1

                documents[cont_files]['length'] = cont_words
                documents[cont_files][description]=description
                documents[cont_files]['terms'] = len(documents[cont_files]['pairs'])
                cont_files += 1

    calculate_idfi(vocabulary,len(documents))
    print(str(cont_words))
    print("Nombre: " + str(nombre))
    print("Ruta completa del archivo: " + str(root))
    print("Número de documentos de la colección " + str(cont_files))
    
    sum_length=0
    for key, value in documents.items():
        sum_length+=value['length']
    print("Longitud de promedio: " + str(sum_length / len(documents)))

    print(vocabulary)

def updateVocabulary(vocabulary,word):
    if(word in vocabulary):
        vocabulary[word]['n_i']= vocabulary[word]['n_i'] +1
    else:
        vocabulary[word]= {'n_i':1}

def calculate_idfi(vocabulary,N):
    for word in vocabulary.keys():
        if(vocabulary[word]['n_i']>=N/2):
            vocabulary[word]['idfi']=0
        else:
            vocabulary[word]['idfi'] = math.log((N-vocabulary[word]['n_i']-0.5)/(vocabulary[word]['n_i']-0.5),2)

###########  Normalize #################
def normalize(text):
    #Funcion: este metodo sirve para normalizar el texto que se recibe.
    #Parametros: String.
    #Resultado: String normalizado de acuerdo a los criterios.

    text_lower = text.lower()
    text_unaccent = remove_accent(text_lower)
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

def read_stopwords():
    #Funcion: este metodo carga y enlista los stopwords.
    #Parametros: No hay.
    #Resultado: Lista de stopwords
    stopwords = []

    with open('stopwords.txt') as f:
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
    if word[0] == "-" and word[1] == "-":
        return [word[2:],"@" + word[2:]]
    return word


def splitpoints(word):
    #Funcion: Divide las palabras con puntos y elimina los que son solo numeros.
    #Parametros: Palabra o string
    #Resultado: Lista con terminos.

    x = re.search("[a-zA-Z]", word)
    word_splited = []
    result = []
    if "." in word:
        if x:
            word_splited = word.split(".")
        for i in word_splited:
            if i.isnumeric()==False:
                result.append(i)
    else:
        result.append(word)
    return result

#####################################

indexColection()