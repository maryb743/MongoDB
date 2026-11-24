from pymongo import MongoClient
#display mongo docs in json format 
from bson.json_util import dumps

#connect to mongodb
client = MongoClient("mongodb://localhost:27017/")

#use movie database and collection
db = client["MovieDB"]
movies = db["movies"]

#Q1 select all movies
print("\nQUERY 1 All movies")

result = movies.find({})

#indent to make output readable
print(dumps(result, indent=4))

#query 2 select horror movies
print("\nQUERY 2 Horror movies")

result = movies.find({"genres": "Horror"})

print(dumps(result, indent=4))

#query 3 projection (selecting specific fields)
print("\nQUERY 3 Movie titles and ratings")

result = movies.find(
    {},
    {"_id": 0, "title": 1, "rating": 1}
)

print(dumps(result, indent=4))