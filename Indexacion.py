from os import walk

def coleccion():

    root = input("Ingrese la ruta completa del archivo: ")
    nombre = root.split("/")[-1]

    totalFiles = 0
    cont_words = 0

    for (dirpath, dirs, files) in walk(root):

        for file in files:
            totalFiles += 1
            with open(dirpath+file, "r") as file:
                for line in file: 
                    for word in line.split(): 
                        cont_words = cont_words + 1
    print(str(cont_words))
    print("Nombre: " + str(nombre))
    print("Ruta completa del archivo: " + str(root))
    print("Número de documentos de la colección " + str(totalFiles))
    #print("Longitud de promedio: " + str(cont_words))
    

coleccion()