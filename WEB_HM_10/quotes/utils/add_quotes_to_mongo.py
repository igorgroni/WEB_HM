import json 

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost/")

db = client.hm10

with open('quotes.json', 'r') as fd:
    quotes = json.load(fd)


for quote in quotes:
    author = db.authors.find_one({'fullname':quote['author']})
    if author:
        db.quotes.insert_one({
            'quote': quote['quote'],
            'tag':quote['tags'],
            'author': ObjectId(author['_id'])
        })

print('procces finished')