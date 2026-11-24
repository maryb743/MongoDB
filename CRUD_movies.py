#connect to mongodb
from pymongo import MongoClient
from bson.json_util import dumps

#connect to mongo
client = MongoClient("mongodb://localhost:27017/")

#use movie database
db = client["MovieDB"]

#use movie collection
movies = db["movies"]

#Create movie
newMovie = {
    "title": "Test Movie",
    "year": "(2026)",
    "genres": ["Comedy", "Adventure"],
    "rating": 7.5,
    "description": "best movie ever",
    "directors": ["Mary Byrne"],
    "cast": ["Rowan Slevin", "Nathan Mills"],
    "votes": 100,
    "runtime": 95,
    "gross": 500000.0
}

result = movies.insert_one(newMovie)

#store the ID of the inserted movie
movieId = result.inserted_id

print("\nNew movie:")
print(dumps(movies.find_one({"_id": movieId}), indent=4))

#update the rating of a movie
movies.update_one(
    
    {"_id": movieId},
    {"$set": {"rating": 9.0}}
    
)

#display updated movie
print("\nUpdated movie:")
print(dumps(movies.find_one({"_id": movieId}), indent=4))

#delete movie
result = movies.delete_one({"_id": movieId})

#confirm deletion
print("\nMovies deleted:", result.deleted_count)

print("Search for deleted movie:")
print(movies.find_one({"_id": movieId}))

#close connection
client.close()