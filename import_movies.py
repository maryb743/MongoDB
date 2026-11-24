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

#list to store all movie documents
movieDocuments = []

#track unique movies using title and year and keep count
#uniqueMovies = set()
#duplicateCount = 0

#open CSV file
with open("movies.csv", "r", encoding="utf-8-sig", newline="") as file:

    reader = csv.DictReader(file)

    #loop through every movie
    for movie in reader:

        #convert genres into an array
        genreText = movie["GENRE"]

        genres = [
            genre.strip()
            for genre in genreText.split(",")
            if genre.strip()
        ]

        #convert rating into a float
        ratingText = movie["RATING"].strip()

        if ratingText:
            rating = float(ratingText)
        else:
            rating = None

        #separate directors and actors
        castNames = movie["STARS"]

        directors = []
        cast = []

        #separate sections at the pipe symbol
        for section in castNames.split("|"):

            section = section.strip()

            if section.startswith(("Director:", "Directors:")):

                directorNames = section.split(":", 1)[1]

                directors = [
                    name.strip()
                    for name in directorNames.split(",")
                    if name.strip()
                ]

            elif section.startswith(("Star:", "Stars:")):

                castText = section.split(":", 1)[1]

                cast = [
                    name.strip()
                    for name in castText.split(",")
                    if name.strip()
                ]

        #convert votes into an integer
        votesText = movie["VOTES"].replace(",", "").strip()

        if votesText:
            votes = int(votesText)
        else:
            votes = None

        #convert runtime into an integer
        runtimeText = movie["RunTime"].replace("min", "").strip()

        if runtimeText:
            runtime = int(runtimeText)
        else:
            runtime = None

        #convert gross earnings into a number
        grossText = movie["Gross"].replace("$", "").replace(",", "").strip()

        if grossText:

            if grossText.endswith("M"):
                gross = float(grossText[:-1]) * 1000000

            elif grossText.endswith("K"):
                gross = float(grossText[:-1]) * 1000

            else:
                gross = float(grossText)

        else:
            gross = None

        #create movie document
        movieDict = {
            
            "title": movie["MOVIES"].strip(),
            "year": movie["YEAR"].strip(),
            "genres": genres,
            "rating": rating,
            "description": movie["ONE-LINE"].strip(),
            "directors": directors,
            "cast": cast,
            "votes": votes,
            "runtime": runtime,
            "gross": gross
            
        }



#display number of movies processed
print("Movies processed: ", len(movieDocuments))
print("Duplicate movies skipped:", duplicateCount)

#display first movie
if movieDocuments:
    print(movieDocuments[0])

#debugging statements
print("Database:", db.name)
print("Collection:", movies.name)
print("Movies ready to insert:", len(movieDocuments))
print("Existing documents:", movies.count_documents({}))
    
#import all movies from csv into MongoDB
if movieDocuments:
    
    #prevent duplicate insert (error checking)
    if movies.count_documents({}) == 0:

        result = movies.insert_many(movieDocuments)

        print("Movies added to database: ", len(result.inserted_ids))

    else:

        print("Movies have already been added no duplicates allowed!!")

#close connection
client.close()
