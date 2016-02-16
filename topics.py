import pymongo

from gensim import corpora, models, similarities

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

connection=pymongo.MongoClient()
db = connection.texts.dail

def get_speeches():
    r = db.find({"len_toks":{"$gte":10}})
    return r

dictionary = corpora.Dictionary.load('debates.dict')

class DebatesCorpus(object):
    def __iter__(self):
        for speech in get_speeches():
            yield dictionary.doc2bow(speech['tokens'])

def create_dictionary():
    # collect statistics about all tokens
    dictionary = corpora.Dictionary(speech['tokens'] for speech in get_speeches())
    #filter out words that only appear once
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq == 1]
    dictionary.filter_tokens(once_ids)
    dictionary.compactify() # remove gaps in id sequence after words that were removed
    dictionary.save('debates.dict') # store the dictionary, for future reference

def create_bow_corpus():
    debates_bow_corpus = DebatesCorpus()
    #debates_bow_corpus = [v for v in corpus]
    #print(debates_bow_corpus)
    corpora.MmCorpus.serialize('debates_bow_corpus.mm', debates_bow_corpus)

def transform_tfidf():
    debates_bow_corpus = corpora.MmCorpus('debates_bow_corpus.mm')
    tfidf = models.TfidfModel(debates_bow_corpus)
    corpora.MmCorpus.serialize('debates_tfidf_corpus.mm', tfidf[debates_bow_corpus])

def transform_lda():
    debates_tfidf_corpus = corpora.MmCorpus('debates_tfidf_corpus.mm')
    lda = models.ldamodel.LdaModel(corpus=debates_tfidf_corpus, id2word=dictionary, num_topics=100, update_every=1, chunksize=10000, passes=1)
    lda.save("debates_lda.lda")

def main():
    #create_dictionary()
    #create_bow_corpus()
    #transform_tfidf()
    transform_lda()

if __name__ == '__main__':
    main()
