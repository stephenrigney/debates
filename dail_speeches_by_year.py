import requests, pymongo, csv, time

connection=pymongo.MongoClient()
db = connection.texts

exist = "http://localhost:8080/exist/rest/"
xq = "db/data/speeches.xq"

def get_speeches_by_year(year):
    r = requests.get(exist+xq, params={"year":year})
    return r.json()

count = [("year", "count", "time")]

def fix_text(speeches):
    for speech in speeches['speeches']:
        if type(speech['date']) == dict:
            speech['date'] = parser.parse(speech['date']['date'])
        try:
            if type(speech['text']) == str:
                speech['text'] = [speech['text']]
        except KeyError:
            print(speech)
        if speech['text'] is None:
            speech['text'] = []
        speech['text'] = [t for t in speech['text'] if t is not None]    
    return speeches

for year in range(1922, 2016):
    startTime = time.time()
    print("***\nYear:", year)
    speeches = get_speeches_by_year(year)
    print("Speech count:", speeches['count'])
    ins = db.dail.insert_many(speeches['speeches'])
    print("MongoDB insert many success: {}".format(ins.acknowledged))
    print("No. of documents in dail collection: {}".format(db.dail.count()))
    elapsedTime = -time.time()-startTime
    print(elapsedTime)
    count.append((speeches['year'], speeches['count'], elapsedTime))

with open("test.csv", "w") as f:
    c = csv.writer(f)
    c.writerows(count)
