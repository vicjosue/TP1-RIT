# Authors: Victor Camacho Artavia <joscamachoartavia@gmail.com>,
#         Jimmy Mok Zhgen <jimmymokz14@gmail.com>

import argparse
import pickle
from Indexer import Indexer

def cli():
    """
    Handling arguments with argparse
    """
    parser = argparse.ArgumentParser(description='Process queries given a collection',prog='Indexer', usage='%(prog)s [options]')
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-sw', metavar='Stopwords', nargs=1,
                        help='stopwords file', required=True)
    required.add_argument('-c', metavar='Colection', nargs=1,
                        help='Colection file', required=True) 
    parser._action_groups.append(optional) #https://stackoverflow.com/questions/24180527/argparse-required-arguments-listed-under-optional-arguments/24181138
    return parser.parse_args()

def main():
    """
    User terminal interface
    """
    parsed_args = cli()
    indexer = Indexer(parsed_args.sw[0],parsed_args.c[0])
    indexer.index_colection()

    menu=["\nMENU\n\n[c] consultar","[l] leer","[g] guardar","[s] salir"]
    while(True):
        for m in menu:
            print(m)
        user_selection=input(">")
        if(user_selection.lower()=="c" or user_selection=="consultar"):
            print("Número de documentos que serán incluidos en el escalafón")
            num_docs=int(input(">"))
            if(type(num_docs)!=int):
                print("Debe ser un numero!")
                continue
            print("Nombres de los dos archivos de respuesta (html y txt, no incluir la extension)")
            result_name=input(">")
            print("Ruta en que desea guardar el resultado")
            path=int(input(">"))
            print("Que es lo que desea consultar?")
            query=input(">")
            scale = indexer.process_query(query,num_docs,result_name)
            print(scale[:num_docs]) # [(id_archivo,valor_similitud),(...),...]
            ### def gudardar(result,result_name+".txt",path):
            #       if similutud==0:
            #           return
            ## todo: GUARDAR EN ARCHIVO "result_name"

        if(user_selection.lower()=="g" or user_selection=="guardar"):
            name=input("name of file>")
            with open(name, 'wb') as pickle_file:
                pickle.dump(indexer, pickle_file)
        
        if(user_selection.lower()=="l" or user_selection=="leer"):
            name=input("name of file>")
            with open(name, 'rb') as pickle_file:
                indexer = pickle.load(pickle_file)

        if(user_selection.lower()=="s" or user_selection=="salir"):
            break
if __name__ == '__main__':
    main()