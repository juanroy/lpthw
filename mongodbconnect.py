import pymongo
import json

conn = pymongo.MongoClient('localhost', 27017)
db = conn.test
coll = db.restaurants
result = coll.find_one({ 'borough' : 'Brooklyn' }, { 'cuisine' : 1, 'name' : 1, '_id' : 0 })
print json.dumps(result)