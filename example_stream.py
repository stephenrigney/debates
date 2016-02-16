from pymongo import Connection

import nltk

import logging, sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from nltk.stem.wordnet import WordNetLemmatizer
import os
from gensim import corpora, models, similarities
from nltk.corpus import stopwords

ENGLISH_STOPWORDS = set(nltk.corpus.stopwords.words('english'))
NON_ENGLISH_STOPWORDS = set(nltk.corpus.stopwords.words()) - ENGLISH_STOPWORDS

def is_english(text):
    text = text.lower()
    words = set(nltk.wordpunct_tokenize(text))
    intersect = len(words & ENGLISH_STOPWORDS)
    return  intersect > len(words & NON_ENGLISH_STOPWORDS) & intersect > 0 #&


lmtzr = WordNetLemmatizer()

def tokenize(document):
    return [lmtzr.lemmatize(word) for word in document.lower().split() if word not in stopwords.words('english') and word.isalpha() and len(word) > 3]

class MyCorpus(corpora.TextCorpus):
    def get_texts(self):
        count = 0
        for app in self.input:
            if count > 200000:
                break
            descr = app [u'results'][0][u'description']
            if is_english(descr):
                    count += 1
                    yield tokenize(descr)

connection = Connection('localhost', 27017)

db = connection.test

myCorpus = MyCorpus(db.iapps.find())

myCorpus.dictionary.filter_extremes(no_below=50, no_above=0.5)
myCorpus.dictionary.compactify()

myCorpus.dictionary.save('/home/vendi/Desktop/iapps/Analysis/pub2.dict') # store the dictionary, for future reference
corpora.BleiCorpus.serialize('/home/vendi/Desktop/iapps/Analysis/pub2.mm', myCorpus)
