# Authors: Victor Camacho Artavia <joscamachoartavia@gmail.com>,
#         Jimmy Mok Zhgen <jimmymokz14@gmail.com>

from os import walk
import math
import webbrowser
from tabulate import tabulate

from ranking_functions import BM25
from utils import  read_stopwords, check_point, double_line, splitpoints, delete_characters, process_line, process_term

class Indexer(object):
    """
    A search engine that indexes a collection to make querys 
    and show information of the files.
    """
    def __init__(self,stopwords,collection_path,model="BM25"):
        """
        Parameters
        ----------
        stopwords: Str
            The path of a file that contains the words that will not be usable
            like prepositions.
        collection_path: Str
            Path of the collection that will be indexed.
        model: Str
            Ranking function for the collection
        """
        self.archive={
            'model':model,
            'documents': {},
            'vocabulary' : {},
            'path':collection_path,
            'average_length':0,
            'name' : collection_path.split("/")[-1],
            'stopwords': read_stopwords(stopwords)
        }
    
    def show_file_data(self,file_id):
        """
        Show all corresponding data from a selected file

        Parameters
        ----------
        file_id: int
            Selected id of the file to show
        """
        headers=["Palabra","n_i"]
        print(tabulate([(k,)+tuple(str(v)) for k,v in self.archive['documents'][file_id]['pairs'].items()],headers=headers))
        print()
        print("Ruta: " + self.archive['documents'][file_id]['path']) 
        print("Nombre: " + self.archive['documents'][file_id]['name']) 
        print("Largo: " + str(self.archive['documents'][file_id]['length'])) 
        print("Descripcion: " + self.archive['documents'][file_id]['description']) 
        print("terminos: " + str(self.archive['documents'][file_id]['terms']))
        
    
    def show_term(self,term):
        
        """
        Show the data from 5 termns above, the termn and 5 under alphabetically

        Parameters
        ----------
        file_id: int
            Selected term to show
        """
        sorted_dict = sorted(self.archive['vocabulary']) #dict_sort is a list
        term=process_term(term)
        print(term)
        try:
            index = sorted_dict.index(term)
            print("n_i: "+ str(self.archive['vocabulary'][term]['n_i']))
            print("idf_i: "+ str(self.archive['vocabulary'][term]['idfi']))
            print("5 anteriores: "+ str(sorted_dict[index-5:index]))
            print("5 posteriores: "+str(sorted_dict[index+1:index+6]))
        except:
            print("term not found")

    def index_colection(self):
        """
        Indexes the collection with the define parameters
        """
        cont_files = 0
        
        for (dirpath, dirs, files) in walk(self.archive['name']):
            relative_path='.'+ dirpath.split(self.archive['name'])[-1] + '\\'
            print("actual folder: "+dirpath)
            for file in files:
                with open(dirpath+'\\'+file, "r") as file:
                    
                    self.archive['documents'][cont_files]= {'path': relative_path,'name':file.name.split("\\")[-1], 'pairs': {}}
                    cont_words = 0
                    cont_description_words=202
                    description=""
                    for line in file:
                        words = process_line(line, self.archive['stopwords'])
                        for word in words:
                            if cont_description_words<200:
                                if(word=="OPTIONS"):
                                    cont_description_words=203
                                else:
                                    cont_description_words+=1
                                    description+=word+" "

                            if("DESCRIPCION"==word or "DESCRIPTION"==word):
                                if(cont_description_words==202): # if it is 203 the file already has a description
                                    cont_description_words=0

                            cont_words = cont_words + 1
    
                            if(word not in self.archive['documents'][cont_files]['pairs']):
                                self.archive['documents'][cont_files]['pairs'][word] = 1
                                self.update_vocabulary(word)
    
                            else:
                                self.archive['documents'][cont_files]['pairs'][word] = self.archive['documents'][cont_files]['pairs'][word]+1
                    
                    self.archive['documents'][cont_files]['length'] = cont_words
                    self.archive['documents'][cont_files]['description']=description
                    self.archive['documents'][cont_files]['terms'] = len(self.archive['documents'][cont_files]['pairs'])
                    cont_files += 1
    
        self.calculate_idfi()
        print("Número de documentos de la colección " + str(cont_files))
        
        sum_length=0
        for key, value in self.archive['documents'].items():
            sum_length+=value['length']
        self.archive['average_length']=sum_length / len(self.archive['documents'])
    
    def update_vocabulary(self,word):
        """
        Parameters
        ----------
        word: Str
            If a word is new in a document then sums 1 or add a new one to the global counter
            of words, this is required by the ranking functions
        """
        if(word in self.archive['vocabulary']):
            self.archive['vocabulary'][word]['n_i']= self.archive['vocabulary'][word]['n_i'] +1
        else:
            self.archive['vocabulary'][word]= {'n_i':1}
    
    def calculate_idfi(self):
        """
        Once added all documents and words we asign their weighs by how much
        unsual is a word
        """
        if(self.archive['model']=="BM25"):
            for word in self.archive['vocabulary'].keys():
                if(self.archive['vocabulary'][word]['n_i']>=len(self.archive['documents'])/2):
                    self.archive['vocabulary'][word]['idfi']=0
                else:
                    self.archive['vocabulary'][word]['idfi'] = math.log(
                        (len(self.archive['documents'])-self.archive['vocabulary'][word]['n_i']-0.5)/
                        (self.archive['vocabulary'][word]['n_i']-0.5),2)
    
    def process_query(self,query,result_name,filename,result_path):
        """
        With a query calcute and make a scale of the best results based on the indexed collection
        
        Parameters
        ----------
        query: Str
            Phrase or word to look for in the indexed documents
        result_name: Str
            Name of the html that contains the scale
        """
        if(self.archive['model']=="BM25"):
            query_dic = self.calculate_query_idfi(query)
            scale = BM25.calculate(self.archive,query_dic)
            scale = list(scale) # example: [(0,0.7),(1,0.5)] -> doc 0 : 0.7 coincidence

        print("Número de documentos que serán incluidos en el html")
        while True:
            num_docs=int(input(">"))
            if(type(num_docs)!=int):
                print("Debe ser un numero!")
            else:
                break

        message = ""
        cont_num_docs = 1
        for similarity in scale:
            #POSISICON escalafón: scale tiene las tuplas ordenadas de mejor posicion a menor
            #Similitud consulta : similarity[1]
            if (cont_num_docs > num_docs):
                break
            path= self.archive['documents'][similarity[0]]['path']    #Ruta 
            first_words = self.archive['documents'][similarity[0]]['description']    #PRIMEROS 200 caracteres
            name = self.archive['documents'][similarity[0]]['name']) 

            message = message + """
                    <ul>
                        <li><B>Nombre:</B> """+str(name)+"""</li>
                        <li><B>Posición:</B> """+str(similarity[0])+"""</li>
                        <li><B>Similitud:</B> """+str(similarity[1])+"""</li>
                        <li><B>Ruta:</B> """+str(path)+"""</li>
                        <li><B>DESCRIPCIÓN:</B> """+str(first_words)+"""</li>
                    </ul>
                    <br></br>
                    """
            cont_num_docs = cont_num_docs + 1
        message = "<h1>Escalafon</h1>" + message
        
        with open(str(result_path) +"/"+ str(filename) + '.html','w') as f:
            f.write(message)
            f.close()
       
        webbrowser.open_new_tab(str(filename) + '.html')

        return scale

    def calculate_query_idfi(self,query):
        """
        The bm25 requires to calculate the idf of each word of the query

        Parameters:
        -----------
        query: Str
            Phrase or word to look for in the indexed documents

        Returns
        --------
        query_dic: Dict
            Dictionary with the format -> {word:{"n_i":#,"idfi":#},word2:{...}}
        """
        
        query_dic = {q: {
            "n_i":query.count(q),
            "idfi": 0.0 if(self.archive['vocabulary'].get(q) and self.archive['vocabulary'][q]['n_i']>=len(self.archive['documents'])/2)
                      else math.log((len(self.archive['documents'])- query.count(q) +0.5) /
                            (query.count(q)+0.5),2)
            } for q in set(process_line(query,self.archive['stopwords']))}
        return query_dic