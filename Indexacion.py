from os import walk
import math 

def indexColection():

    root = input("Ingrese la ruta completa del archivo: ")
    nombre = root.split("/")[-1]

    cont_files = 0
    documents = {}
    vocabulary = {}
    
    for (dirpath, dirs, files) in walk(root):
        relative_path='.'+ dirpath.split(root)[-1] + '\\'
        print(relative_path)
        for file in files:
            with open(dirpath+'\\'+file, "r") as file:
                documents[cont_files]= {'path': relative_path,'name':file.name.split("\\")[-1], 'pairs': {}}
                cont_words = 0
                cont_description_words=0
                description=""
                for line in file:
                    for word in line.split():
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
        print(vocabulary[word]['n_i'])
        print(N)
        if(vocabulary[word]['n_i']>=N/2):
            vocabulary[word]['idfi']=0
        else:
            vocabulary[word]['idfi'] = math.log((N-vocabulary[word]['n_i']-0.5)/(vocabulary[word]['n_i']-0.5),2)
    

indexColection()