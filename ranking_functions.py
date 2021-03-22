# Authors: Victor Camacho Artavia <joscamachoartavia@gmail.com>

class BM25(object):
    """
    BM25 (BM is an abbreviation of best matching) is a ranking function used by search engines
    to estimate the relevance of documents to a given search query.
    It is based on the probabilistic retrieval framework -> https://en.wikipedia.org/wiki/Okapi_BM25
    """
    def calculate(archive,query,k=1.2,b=0.75):
        """
        Parameters
        ----------
        archive:
            Procesed collection of the class Indexer
        query:
            Procesed query in a dictionary with the format -> {word:{"n_i":#,"idfi":#},word2:{...}}
        k: float
            Calibrate the frequency scale of the qi term in the D document
        b: float
            Determines the scale of the document length
        """
        scale={}
        for doc_id,doc_data in archive['documents'].items():
            sum=0.0
            for doc_word, doc_word_amount in doc_data['pairs'].items():
                q=query.get(doc_word)
                if q:
                    sum += q['idfi']* (doc_word_amount*(k+1)/
                                     (doc_word_amount + k*(1-b+b*(doc_data['length']/
                                                            archive['average_length'])
                                                    )
                                ))
            scale[doc_id] = sum
        return sorted(scale.items(), key=lambda x: x[1], reverse=True)