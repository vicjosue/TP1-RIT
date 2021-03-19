# Authors: Victor Camacho Artavia <joscamachoartavia@gmail.com>

class BM25(object):=
    def calculate(archive,query,k=1.2,b=0.75):
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