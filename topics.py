import keyring, requests, time
from spacy.tokens.doc import Doc
from spacy.en import English

from lxml import etree
from gensim import corpora, models, similarities

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

start_time = time.time()
#nlp = spacy.en.English()
print("Time to load full spacy library: {}".format(time.time() - start_time))


def tokenize_doc(text):
    doc = [w.lemma_ for w in nlp(text) if w.is_alpha and not w.is_stop]
    return doc
