import os
import pymongo
from cPickle import dumps, loads
from bson.binary import Binary

arr2bson = lambda x: Binary(dumps(x, protocol=2), subtype=128)
bson2arr = lambda x: loads(x)

def getmongodb ():
    MONGO_URI = os.environ.get('MONGOHQ_URL')
    dbname = MONGO_URI.split('/')[-1]

    db = pymongo.MongoClient(MONGO_URI)[dbname]
    return db
