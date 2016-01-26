import pymongo, requests, keyring
from pprint import pprint
from dateutil import parser

'''Retrieves a json formatted list of texts from exist-db which is then inserted in mongodb
Usage: python3 exist-to-mongo.py <path/to/query.xq> (eventually)
'''


connection=pymongo.MongoClient()
db = connection.texts

exist = "http://localhost:8080/exist/rest/"

xq = "/db/data/members_31_dail.xq"

#r = requests.get(exist, params={"_query":xq})
r=requests.get(exist+xq[1:])
print("eXist-db http request status code: {}".format(r.status_code))
members = r.json()['members']
print("Number of documents retrieved: {}".format(len(members)))

print("\n---------------------------------------\n")

print("Example speech document\n")
#example = {'_id':speeches[1]['_id'],
            #"uri":speeches[1]['uri'],
            #"date":speeches[1]['date'],
            #"spkr":speeches[1]['spkr'],
            #"text": ["Paragraph", "Another paragraph"]}
example = members[1].keys()
pprint(example)

print("\n---------------------------------------\n")
ins = db.longford.insert_many(members)
print("MongoDB insert many success: {}".format(ins.acknowledged))
print("No. of documents in MongoDB collection: {}".format(db.longford.count()))
