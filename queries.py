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

#seletc *
result = movies.find({})

#indent to make output readable
print(dumps(result, indent=4))

#Q2 select horror movies
print("\nQUERY 2 Horror movies")

#WHERE in sql
result = movies.find({"genres": "Horror"})

print(dumps(result, indent=4))

#Q3 projection (selecting specific fields)
print("\nQUERY 3 Movie titles and ratings")

result = movies.find(
    {},
    
    {"_id": 0, "title": 1, "rating": 1}
    
)

print(dumps(result, indent=4))

#Q4 sort movies by highest rating
print("\nQUERY 4 - Highest rated movies")

result = movies.find().sort("rating", -1).limit(5)

print(dumps(result, indent=4))

#Q5 display movies with a rating of 8 or higher (aggregate)
print("\nQuery 5 - Movies rated 8 or higher")

#MATCH TO FILTER IF A RATING IS GREATER THAN OR QUAL TO 8
result = movies.aggregate([
    {"$match": {"rating": {"$gte": 8}}}
])

print(dumps(result, indent=4))

#close connection
client.close()