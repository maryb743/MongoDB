#import the MongoDB client from PyMongo (python library connecting it mongo)
from pymongo import MongoClient

#connect to mongo
client = MongoClient("mongodb://localhost:27017/")

#use moviedb
db = client["MovieDB"]

#use movie collection
movies = db["movies"]

#check pythons connection to mongo
client.admin.command("ping")

#validation
print("Successfully connected to MongoDB!")


import csv

#open movie csv file with read permissions
with open("movies.csv", "r", encoding="utf-8-sig", newline="") as file:
    #reader object
    reader = csv.DictReader(file)

    #display first movie in file
    #convert genre to python list to later be embedded array
    first_movie = next(reader)

    #get genres
    genre_text = first_movie["GENRE"]

    #seperate commma-seperated genres into list
    genres = genre_text.split(",")

    #remove whitespace 
    genres = [genre.strip() for genre in genres]
    
    #dictionary to represent one MongoDB movie document
    movie_document = {
        
        "title": first_movie["MOVIES"].strip(),
        "year": first_movie["YEAR"].strip(),
        "genres": genres,
        "rating": None
        
    }

    #display the document
    print(movie_document)

    #show genres
    print("Og genres:", genre_text)
    print("new genres:", genres)
    
#close
client.close()