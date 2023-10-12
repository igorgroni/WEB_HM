import os
import django

from pymongo import MongoClient


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes.settings")
django.setup()

from quotesapp.models import Quote, Tag, Author #noqa
from utils.connect import format_uri


uri = format_uri()

client = MongoClient(uri)

db = client.hm10

authors = db.authors.find()

for author in authors:
    print(author)

