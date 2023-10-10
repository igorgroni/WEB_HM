import json 
import configparser

from pymongo import MongoClient
from bson.objectid import ObjectId

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

client = MongoClient(
    f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority")

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