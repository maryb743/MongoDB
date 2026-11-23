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
    firstMovie = next(reader)

    #get genres
    genreText = firstMovie["GENRE"]

    #seperate commma-seperated genres into list
    genres = genreText.split(",")

    #remove whitespace 
    genres = [genre.strip() for genre in genres]
    
    #movie rating from the CSV
    ratingText = firstMovie["RATING"].strip()

    #convert the rating to a decimal number
    if ratingText:
        
        rating = float(ratingText)
        
    else:
        
        #check for missing rating and set to none
        rating = None
        
        
     #lists for directors and actors
    directors = []
    
    cast = []
    
    #converting votes into integers and accounting for the fact that theres commas in the numbers in the database
    votesText = firstMovie["VOTES"].replace(",", "").strip()
    
    if votesText:
        
        votes = int(votesText.replace(",", ""))
        
    else:
        
        votes = None
    
    #convert runtime into minutes
    runtimeText = firstMovie["RunTime"].replace("min", "").strip()

    if runtimeText:
        
        runtime = int(runtimeText)
        
    else:
        
        runtime = None
        
    #convert gross earnings into float 
    grossText = firstMovie["Gross"].replace("$", "").strip()

    if grossText:
        
        if grossText.endswith("M"):
            
            #remove the letter and convert into whole number 
            gross = float(grossText[:-1]) * 1000000
            
        elif grossText.endswith("K"):
            
             #remove the letter and convert into whole number 
            gross = float(grossText[:-1]) * 1000
            
        else:
            
            gross = float(grossText)
        
    else:
        
        gross = None

    #movie document
    movieDict = {
        
    "title": firstMovie["MOVIES"].strip(),
    "year": firstMovie["YEAR"].strip(),
    "genres": genres,
    "rating": rating,
    #changed blank one line column to description field in mongodb
    "description": firstMovie["ONE-LINE"].strip(),
    "directors": directors,
    "cast": cast,
    "votes": votes,
    "runtime": runtime,
    "gross": gross
    }

    #display the document
    print(movieDict)
    
    #display og stars info
    castNames = firstMovie["STARS"]

    #separating the director section from the actors section
    sections = castNames.split("Stars: ")

    #get director names
    directorNames = sections[0].replace("Director: ", "").strip()

    #put directors into a list
    directors = [name.strip() for name in directorNames.split(",") if name.strip()]

    #get the actor names if a Stars section exists
    if len(sections) > 1:
        
        cast_text = sections[1].strip()
        
        cast = [name.strip() 
                #seperate names at commas
                for name in cast_text.split(",") 
                #remove white space
                if name.strip()]

    print(movieDict)
    
    ''' #display the results
    print("Directors: ", directors)
    print("Cast: ", cast)
    #og stars column with directors and cast together
    print("Og STARS data: ")
    print(castNames)

    print("Og genres: ", genreText)
    print("new genres: ", genres) 
    
    '''
    
#close
client.close()
