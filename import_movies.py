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
    
    #movie rating from the CSV
    rating_text = first_movie["RATING"].strip()

    #convert the rating to a decimal number
    if rating_text:
        
        rating = float(rating_text)
        
    else:
        
        #check for missing rating and set to none
        rating = None
        
        
     #lists for directors and actors
    directors = []
    cast = []
        
    #dictionary to represent one MongoDB movie document
    movie_dict = {
        
    "title": first_movie["MOVIES"].strip(),
    "year": first_movie["YEAR"].strip(),
    "genres": genres,
    "rating": rating,
    #changed blank one line column to description field in mongodb
    "description": first_movie["ONE-LINE"].strip(),
    "directors": directors,
    "cast": cast
    }

    #display the document
    print(movie_dict)
    
    #display og stars info
    stars_names = first_movie["STARS"]

    #separating the director section from the actors section
    sections = stars_names.split("Stars: ")

    #get director names
    director_names = sections[0].replace("Director: ", "").strip()

    #put directors into a list
    directors = [name.strip() for name in director_names.split(",") if name.strip()]

    #get the actor names if a Stars section exists
    if len(sections) > 1:
        
        cast_text = sections[1].strip()
        
        cast = [name.strip() 
                #seperate names at commas
                for name in cast_text.split(",") 
                #remove white space
                if name.strip()]

    #display the results
    print("Directors: ", directors)
    print("Cast: ", cast)
    #og stars column with directors and cast together
    print("Og STARS data: ")
    print(stars_names)

    print("Og genres: ", genre_text)
    print("new genres: ", genres)
    
#close
client.close()
