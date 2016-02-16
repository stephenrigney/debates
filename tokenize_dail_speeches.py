from spacy.en import English
import time, pymongo, re, datetime
from sys import argv
from dateutil import parser, relativedelta

connection=pymongo.MongoClient()
db = connection.texts.dail

print("loading spaCy English corpus")
startTime = time.time()
NLP = English()
print("Spacy English loaded in {} sec".format(time.time()-startTime))

def tokenize_doc(text):
    doc = NLP(text)
    toks = [w.lemma_ for w in doc if w.is_alpha and not w.is_stop]
    return doc, toks

def find_speeches(dates):
    startTime = time.time()
    print("Retrieving speeches from {} until {}".format(dates["$gte"].date(), dates['$lt'].date()))
    speeches = db.find({"date":dates})
    count = speeches.count()
    print("Retrieved {} speeches in {} sec".format(count, time.time()-startTime))
    return speeches

def tokenize_speeches(speeches):
    for speech in speeches:
        startTime = time.time()
        print("---\n", speech["uri"])
        text = "".join(speech["text"])
        doc, toks = tokenize_doc(text)
        speech["byte_string"]= doc.to_bytes()
        speech['tokens'] = toks
        speech["len_doc"] = len(doc)
        speech['len_toks'] = len(toks)
        up = db.update_one({"_id":speech["_id"]}, {"$set":speech})
        #print(up.acknowledged)
        print("Processed in {} sec: tokens: {} doc: {}".format(time.time()-startTime, speech['len_doc'], speech['len_toks']))

def main():
    startTime = time.time()
    start = "1934-01-01"
    length = 82
    start_date = parser.parse(start)
    end_date = start_date+relativedelta.relativedelta(years=length)
    speeches = find_speeches({"$gte":start_date, "$lt":end_date})
    tokenize_speeches(speeches)
    print("Total processing time: {} min".format((time.time()-startTime)/60))



if __name__ == '__main__':
    main()
