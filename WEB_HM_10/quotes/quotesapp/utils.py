from pymongo import MongoClient
from utils.connect import main


def get_mongo_db():
    client = main()

    db = client.hm10
    return db
