import gensim
import pyLDAvis
import pyLDAvis.gensim

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary = gensim.corpora.Dictionary.load('debates.dict')
corpus = gensim.corpora.MmCorpus('debates_tfidf_corpus.mm')
lda = gensim.models.ldamodel.LdaModel.load('debates_lda.lda')

debates_vis_data = pyLDAvis.gensim.prepare(lda, corpus, dictionary)

pyLDAvis.save_html(debates_vis_data, "debates_lda.html")
