from os import walk

def coleccion():
    root = input("Ingrese la ruta del archivo: ")
    for (dirpath, dirnames, filenames) in walk(root):
        print(dirpath)
        print(dirnames)
        print(filenames)

coleccion()