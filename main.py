# Authors: Victor Camacho Artavia <joscamachoartavia@gmail.com>,
#         Jimmy Mok Zhgen <jimmymokz14@gmail.com>

import argparse
import pickle
from Indexer import Indexer
from tabulate import tabulate

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

    menu=["\nMENU\n\n[c] consultar","[a] inspeccionar archivo",
            "[i] inspeccionar indice/termino","[l] leer","[g] guardar","[s] salir"]

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
            path=input(">")
            print("Que es lo que desea consultar?")
            query=input(">")
            scale = indexer.process_query(query,result_name)
            print(scale[:num_docs]) # [(id_archivo,valor_similitud),(...),...]

            list_scales = []
            for i in scale[:num_docs]:
                if i[1] != 0: 
                    list_scales.append(i)
            with open(path +"/"+ result_name + '.txt', 'w') as f:
                f.write(tabulate([("ID","Similitud")] + list_scales))
        
        if(user_selection.lower()=="a" or user_selection=="inspeccionar archivo"):
            print("Cual es el id del archivo que desea consultar?")
            file_id=int(input(">"))
            if(type(file_id)!=int):
                print("Debe ser un numero!")
                continue
            indexer.show_file_data(file_id)

        if(user_selection.lower()=="i" or user_selection=="inspeccionar indice/termino"):
            print("Escriba el nombre del termino que desea inspeccionar")
            term=int(input(">"))
            indexer.show_term(term)

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